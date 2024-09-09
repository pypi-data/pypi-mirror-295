#!/usr/bin/env python3
# -*- coding: utf - 8 -* -
from typing import NamedTuple, List, Union, TYPE_CHECKING

from refinery.units import Arg, Unit
from refinery.lib.vfs import VirtualFileSystem, VirtualFile
from refinery.lib.structures import MemoryFile
from refinery.lib.tools import NoLogging

import logging

if TYPE_CHECKING:
    from ipaddress import IPv4Address, IPv6Address
    from pcapkit.foundation.reassembly.data.tcp import Datagram
    TIPAddr = Union[IPv4Address, IPv6Address]


class Conversation(NamedTuple):
    src_addr: str
    dst_addr: str
    src_port: int
    dst_port: int

    @classmethod
    def FromID(cls, stream_id):
        src, sp = stream_id.src
        dst, dp = stream_id.dst
        return cls(str(src), str(dst), sp, dp)

    @property
    def src(self):
        return F'{self.src_addr}:{self.src_port}'

    @property
    def dst(self):
        return F'{self.dst_addr}:{self.dst_port}'

    def __hash__(self):
        return hash(frozenset((self.src, self.dst)))

    def swapped(self):
        cls = self.__class__
        return cls(self.dst_addr, self.src_addr, self.dst_port, self.src_port)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return F'[{self.src}] --> [{self.dst}]'

    def src_to_dst(self):
        return {'src': self.src, 'dst': self.dst}

    def dst_to_src(self):
        return {'src': self.dst, 'dst': self.src}


class pcap(Unit):
    """
    Performs TCP stream reassembly from packet capture (PCAP) files. By default, the unit emits the parts of
    each TCP conversation, attaching several pieces of metadata to each such output: Included are the source
    and destination socket address as well as the variable `stream` which identifies the conversation which
    it was part of. The chunks are returned in the order that the bytes were exchanged between source and
    destination. When the `--merge` parameter is specified, the unit instead collects all bytes going forward
    and backwards, respectively, and emitting these as two chunks, for each TCP conversation that took place.
    """

    def __init__(self, merge: Arg.Switch('-m', help='Merge both parts of each TCP conversation into one chunk.') = False):
        super().__init__(merge=merge)

    @Unit.Requires('pypcapkit[scapy]>=1.3', 'all')
    def _pcapkit():
        import scapy.layers.tls.session # noqa
        import pcapkit
        return pcapkit

    def process(self, data):
        with NoLogging():
            pcapkit = self._pcapkit
            logging.getLogger('pcapkit').disabled = True

        merge = self.args.merge

        with NoLogging(), VirtualFileSystem() as fs:
            vf = VirtualFile(fs, data, 'pcap')
            extraction = pcapkit.extract(
                fin=vf.path, engine='scapy', store=False, nofile=True, extension=False, tcp=True, reassembly=True, reasm_strict=True)
            tcp: List[Datagram] = list(extraction.reassembly.tcp)

        tcp.sort(key=lambda p: min(p.index, default=0))

        count, convo = 0, None
        src_buffer = MemoryFile()
        dst_buffer = MemoryFile()
        for datagram in tcp:
            this_convo = Conversation.FromID(datagram.id)
            if this_convo != convo:
                if count and merge:
                    if src_buffer.tell():
                        yield self.labelled(src_buffer.getvalue(), **convo.src_to_dst())
                        src_buffer.truncate(0)
                    if dst_buffer.tell():
                        yield self.labelled(dst_buffer.getvalue(), **convo.dst_to_src())
                        dst_buffer.truncate(0)
                count = count + 1
                convo = this_convo
            for data in datagram.packet:
                if not merge:
                    yield self.labelled(data, **this_convo.src_to_dst(), stream=count)
                elif this_convo.src == convo.src:
                    src_buffer.write(data)
                elif this_convo.dst == convo.src:
                    dst_buffer.write(data)
                else:
                    raise RuntimeError(F'direction of packet {convo!s} in conversation {count} is unknown')

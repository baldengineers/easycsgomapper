import struct
from binascii import crc32
from io import FileIO
from io import open as fopen
import os

__version__ = "0.12"
__author__ = "Rossen Georgiev"


def open(vpk_path, **kwargs):
    """
    Returns a VPK instance for specified path. Same argumets as VPK class.
    """
    return VPK(vpk_path, **kwargs)


def new(dir_path):
    """
    Returns a NewVPK instance for the specific path.
    """
    return NewVPK(dir_path)


class NewVPK:
    def __init__(self, path):
        self.signature = 0x55aa1234
        self.version = 1
        self.tree_length = 0
        self.header_length = 4*3

        self.tree = {}
        self.path = ''
        self.file_count = 0

        self.read_dir(path)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.path)

    def read_dir(self, path):
        """
        Reads the given path into the tree
        """
        self.tree = {}
        self.file_count = 0
        self.path = path

        for root, _, filelist in os.walk(path):
            rel = root[len(path):].lstrip('/')

            # empty rel, means file is in root dir
            if not rel:
                rel = ' '

            for filename in filelist:
                filename = filename.split('.')
                if len(filename) <= 1:
                    raise RuntimeError("Files without an extension are not supported: {0}".format(
                                       repr(os.path.join(root, '.'.join(filename))),
                                       ))

                ext = filename[-1]
                filename = '.'.join(filename[:-1])

                if ext not in self.tree:
                    self.tree[ext] = {}
                if rel not in self.tree[ext]:
                    self.tree[ext][rel] = []

                self.tree[ext][rel].append(filename)
                self.file_count += 1

        self.tree_length = self.calculate_tree_length()


    def calculate_tree_length(self):
        """
        Walks the tree and calculate the tree length
        """
        tree_length = 0

        for ext in self.tree:
            tree_length += len(ext) + 2

            for relpath in self.tree[ext]:
                tree_length += len(relpath) + 2

                for filename in self.tree[ext][relpath]:
                    tree_length += len(filename) + 1 + 18

        return tree_length + 1


    def save(self, vpk_output_path):
        """
        Saves the VPK at the given path
        """
        with fopen(vpk_output_path, 'wb') as f:
            # write VPK1 header
            f.write(struct.pack("3I", self.signature,
                                      self.version,
                                      self.tree_length))

            self.header_length = f.tell()

            data_offset = self.header_length + self.tree_length

            # write file tree
            for ext in self.tree:
                f.write("{0}\x00".format(ext).encode('latin-1'))

                for relpath in self.tree[ext]:
                    f.write("{0}\x00".format(relpath).encode('latin-1'))

                    for filename in self.tree[ext][relpath]:
                        f.write("{0}\x00".format(filename).encode('latin-1'))

                        # append file data
                        metadata_offset = f.tell()
                        file_offset = data_offset
                        real_filename = filename if not ext else "{0}.{1}".format(filename, ext)
                        checksum = 0
                        f.seek(data_offset)

                        with fopen(os.path.join(self.path,
                                                '' if relpath == ' ' else relpath,
                                                real_filename
                                                ),
                                   'rb') as pakfile:
                            for chunk in iter(lambda: pakfile.read(1024), b''):
                                checksum = crc32(chunk, checksum)
                                f.write(chunk)

                        data_offset = f.tell()
                        file_length = f.tell() - file_offset
                        f.seek(metadata_offset)

                        # metadata

                        # crc32
                        # preload_length
                        # archive_index
                        # archive_offset
                        # file_length
                        # term
                        f.write(struct.pack("IHHIIH", checksum & 0xFFffFFff,
                                                      0,
                                                      0x7fff,
                                                      file_offset - self.tree_length - self.header_length,
                                                      file_length,
                                                      0xffff
                                                      ))


                    # next relpath
                    f.write(b"\x00")
                # next ext
                f.write(b"\x00")
            # end of file tree
            f.write(b"\x00")


    def save_and_open(self, path):
        """
        Saves the VPK file and returns VPK instance of it
        """
        self.save(path)
        return VPK(path)


class VPK:
    """
    Wrapper for reading Valve's VPK files
    """

    def __init__(self, vpk_path, read_header_only=False):
        # header
        self.signature = 0
        self.version = 0
        self.tree_length = 0
        self.header_length = 0

        self.tree = {}
        self.vpk_path = vpk_path

        self.read_header()

        if not read_header_only:
            self.read_index()

    def __repr__(self):
        headonly = ', read_header_only=True' if len(self) == 0 else ''
        return "%s('%s'%s)" % (self.__class__.__name__, self.vpk_path, headonly)

    def __iter__(self):
        return self.tree.__iter__()

    def items(self):
        def items_generator(tree):
            for path in tree:
                yield path, self.get_file_meta(path)

        return items_generator(self.tree)

    def __len__(self):
        return len(self.tree)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _read_sz(self, f):
        buf = b''

        for chunk in iter(lambda: f.read(64), b''):
            pos = chunk.find(b'\x00')
            if pos > -1:
                buf += chunk[:pos]
                f.seek(f.tell() - (len(chunk) - (pos + 1)))
                break

            buf += chunk

        return buf.decode('ascii')

    def __getitem__(self, key):
        """
        Returns VPKFile instance
        """
        return self.get_file(key)

    def get_file(self, path):
        """
        Returns VPKFile instance for the given path
        """
        metadata = self.get_file_meta(path)
        return VPKFile(self.vpk_path, filepath=path, **metadata)

    def get_file_meta(self, path):
        """
        Returns metadata for given file path
        """
        if path not in self.tree:
            raise KeyError("Path doesn't exist")

        return dict(zip(['preload',
                         'crc32',
                         'preload_length',
                         'archive_index',
                         'archive_offset',
                         'file_length',
                         ], self.tree[path]))

    def read_header(self):
        """
        Reads VPK file header from the file
        """
        with fopen(self.vpk_path, 'rb') as f:
            (self.signature,
             self.version,
             self.tree_length
             ) = struct.unpack("3I", f.read(3*4))

            # original format - headerless
            if self.signature != 0x55aa1234:
                self.signature = 0
                self.version = 0
                self.tree_length = 0
            # v1
            elif self.version == 1:
                self.header_length += 4*3
            # v2 with extended header
            #
            # according to http://forum.xentax.com/viewtopic.php?f=10&t=11208
            # struct VPKDirHeader_t
            # {
            #    int32 m_nHeaderMarker;
            #    int32 m_nVersion;
            #    int32 m_nDirectorySize;
            #    int32 m_nEmbeddedChunkSize;
            #    int32 m_nChunkHashesSize;
            #    int32 m_nSelfHashesSize;
            #    int32 m_nSignatureSize;
            # }
            elif self.version == 2:
                (self.embed_chunk_length,
                 self.chunk_hashes_length,
                 self.self_hashes_length,
                 self.signature_length
                 ) = struct.unpack("4I", f.read(4*4))
                self.header_length += 4*7
            else:
                raise ValueError("Invalid header, or unsupported version")

    def read_index(self):
        """
        Reads the index and populates the directory tree
        """

        self.tree = {}
        with fopen(self.vpk_path, 'rb') as f:
            f.seek(self.header_length)

            while True:
                if self.version > 0 and f.tell() > self.tree_length + self.header_length:
                    raise ValueError("Error parsing index (out of bounds)")

                ext = self._read_sz(f)
                if ext == '':
                    break

                while True:
                    path = self._read_sz(f)
                    if path == '':
                        break
                    if path != ' ':
                        path += '/'
                    else:
                        path = ''

                    while True:
                        name = self._read_sz(f)
                        if name == '':
                            break

                        # crc32
                        # preload_length
                        # archive_index
                        # archive_offset
                        # file_length
                        metadata = list(struct.unpack("IHHII", f.read(16)))

                        if struct.unpack("H", f.read(2))[0] != 0xffff:
                            raise ValueError("Error while parsing index")

                        if metadata[2] == 0x7fff:
                            metadata[3] += self.header_length + self.tree_length

                        metadata.insert(0, f.read(metadata[1]))

                        self.tree["{0}{1}.{2}".format(path, name, ext)] = tuple(metadata)


class VPKFile(FileIO):
    """
    Wrapper class for files with VPK

    Should act like a regular file object. No garantees
    """

    def __init__(self, vpk_path, **kw):
        self.vpk_path = vpk_path
        self.vpk_meta = kw

        for k, v in kw.items():
            setattr(self, k, v)

        if self.vpk_meta['preload'] != b'':
            self.vpk_meta['preload'] = '...'

        # total file length
        self.length = self.preload_length + self.file_length
        # offset of entire file
        self.offset = 0

        if self.file_length == 0:
            self.vpk_path = None
            return

        super(VPKFile, self).__init__(vpk_path.replace("dir.", "%03d." % self.archive_index), 'rb')
        super(VPKFile, self).seek(self.archive_offset)

    def save(self, path):
        """
        Save the file to the specified path
        """
        # remember and restore file position
        pos = self.tell()
        self.seek(0)

        with fopen(path, 'wb') as output:
            output.truncate(self.length)
            for chunk in iter(lambda: self.read(1024), b''):
                output.write(chunk)

        self.seek(pos)

    def verify(self):
        """
        Returns True if the file contents match with the CRC32 attribute

        note: reset
        """

        # remember file pointer
        pos = self.tell()
        self.seek(0)

        checksum = 0
        for chunk in iter(lambda: self.read(1024), b''):
            checksum = crc32(chunk, checksum)

        # restore file pointer
        self.seek(pos)

        return self.crc32 == checksum & 0xffffffff

    def __repr__(self):
        return "%s(%s, %s)" % (
            self.__class__.__name__,
            repr(self.name) if self.file_length > 0 else None,
            ', '.join(["%s=%s" % (k, repr(v)) for k, v in self.vpk_meta.items()])
            )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        line = self.readline()
        if line == b'':
            raise StopIteration
        return line

    def close(self):
        super(VPKFile, self).close()

    def tell(self):
        return self.offset

    def seek(self, offset):
        if offset < 0:
            raise IOError("Invalid argument")

        self.offset = offset
        if self.file_length > 0:
            super(VPKFile, self).seek(self.archive_offset + max(offset - self.preload_length, 0))

    def readlines(self):
        return [line for line in self]

    def readline(self, a=False):
        buf = b''

        for chunk in iter(lambda: self.read(256), b''):
            pos = chunk.find(b'\n')
            if pos > -1:
                pos += 1  # include \n
                buf += chunk[:pos]
                self.seek(self.offset - (len(chunk) - pos))
                break

            buf += chunk

        return buf

    def read(self, length=-1):
        if length == 0 or self.offset >= self.length:
            return b''

        data = b''

        if self.offset <= self.preload_length:
            data += self.preload[self.offset:self.offset+length if length > -1 else None]
            self.offset += len(data)
            if length > 0:
                length = max(length - len(data), 0)

        if self.file_length > 0 and self.offset >= self.preload_length:
            left = self.file_length - (self.offset - self.preload_length)
            data += super(VPKFile, self).read(left if length == -1 else min(left, length))
            self.offset += left if length == -1 else min(left, length)

        return data

    def write(self, seq):
        raise NotImplementedError("write method is not supported")

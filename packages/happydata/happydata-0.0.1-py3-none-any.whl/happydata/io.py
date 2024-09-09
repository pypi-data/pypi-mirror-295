import json,os,gzip,io,tarfile,zipfile
from typing import List,Dict,Iterable,Generator,Optional,IO,Tuple,BinaryIO
from pathlib import Path

def to_jsonl(l: Iterable, to:str):
    with open(to, 'w') as f:
        for item in l:
            f.write(json.dumps(item, ensure_ascii=False, default=vars) + '\n')

def from_jsonl(from_file:str |Path| IO)->Generator[Dict,str,None]:
    if isinstance(from_file, str) or isinstance(from_file, Path):
        if str(from_file).endswith('.gz'):
            with gzip.open(from_file, 'rt') as f:
                for line in f:
                    yield json.loads(line)
        else:
            with open(from_file, 'r') as f:
                for line in f:
                    yield json.loads(line)
    else:
        for line in from_file:
            yield json.loads(line)

def to_jsonl_gz(l: Iterable, to:str, add_end=True):
    with gzip.open(to, 'wt') as f:
        for item in l:
            if add_end:
                f.write(json.dumps(item, ensure_ascii=False, default=vars) + '\n')
            else:
                f.write(json.dumps(item, ensure_ascii=False, default=vars))

def from_jsonl_gz(from_file:str|Path| IO)->Generator[Dict,str,None]:
    if isinstance(from_file, str) or isinstance(from_file, Path):
        with gzip.open(from_file, 'rt') as f:
            for line in f:
                yield json.loads(line)
    else:
        for line in from_file:
            yield json.loads(line)

def load_jsonl_gz(from_file:str)->List[Dict]:
    return list(from_jsonl_gz(from_file))


def load_jsonl(from_file:str)->List[Dict]:
    return list(from_jsonl(from_file))

def read_lines(file:str,remove_end=True)->Generator[str,str,None]:
    with open(file, 'r') as f:
        for line in f:
            if remove_end:
                yield line.removesuffix('\n').removesuffix('\r')
            else:
                yield line

def read_lines_gz(file:str,remove_end=True)->Generator[str,str,None]:
    with gzip.open(file, 'rt') as f:
        for line in f:
            if remove_end:
                yield line.removesuffix('\n').removesuffix('\r')
            else:
                yield line

def write_lines(lines:Iterable[str],to:str|Path ,add_end=True):
    with open(to, 'w') as f:
        for line in lines:
            if add_end:
                f.write(line+'\n')
            else:
                f.write(line)


def read_tar_gz(file:str|Path) -> Generator[Tuple[tarfile.TarInfo,IO],str,None]:
    with tarfile.open(file, 'r:gz') as tar:
        for member in tar.getmembers():
            with tar.extractfile(member) as f:
                yield member , f

def write_tar_gz(file:str|Path,files:Dict[str,BinaryIO]):
    with tarfile.open(file, 'w:gz') as tar:
        for name, f in files.items():
            info = tarfile.TarInfo(name)
            buf = f.read()
            info.size = len(buf)
            tar.addfile(info, io.BytesIO(buf))

def read_zip(file:str|Path) -> Generator[Tuple[str,IO],str,None]:
    with zipfile.ZipFile(file, 'r') as z:
        for member in z.namelist():
            with z.open(member) as f:
                yield member , f

def write_zip(file:str|Path,files:Dict[str,BinaryIO]):
    with zipfile.ZipFile(file, 'w') as z:
        for name, f in files.items():
            z.writestr(name, f.read())

def read_str(file:str|Path)->str:
    with open(file, 'r') as f:
        return f.read()

def write_str(s:str,to:str|Path):
    with open(to, 'w') as f:
        f.write(s)

def read_json(file:str|Path)->Dict:
    with open(file, 'r') as f:
        return json.load(f)

def write_json(d:Dict,to:str|Path):
    with open(to, 'w') as f:
        json.dump(d, f)
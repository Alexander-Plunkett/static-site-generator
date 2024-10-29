import os, shutil

def copy_contents(src, dst):
    if not os.path.exists(src):
        raise ValueError("No such path exists")
    if not os.path.exists(dst):
        os.mkdir(dst)
    
    for item in os.listdir(src):
        new_src = os.path.join(src, item)
        if "." in item:
            shutil.copy(new_src, dst)
        else:
            new_dst = os.path.join(dst, item)
            os.mkdir(new_dst)
            copy_contents(new_src, new_dst)
import os, sys, glob
from main import Save_Data

def test():
    work_dir = "/data/home/wuxingxing/datas/PWMLFF_library_data/HfO2/hfo2_dpgen/HfO2_liutheory"
    init_dir = glob.glob(os.path.join(work_dir, "sys.*"))
    init_dir = sorted(init_dir, key=lambda x: int(x.split(".")[-1]))
    for i, d in enumerate(init_dir):
        print(i, d)
        Save_Data(data_path=d,
                datasets_path=os.path.join(work_dir, "new_pwdata"),
                train_ratio = 0.2,
                random=False,
                format="deepmd/npy"
                )

if __name__ == "__main__":
    test()
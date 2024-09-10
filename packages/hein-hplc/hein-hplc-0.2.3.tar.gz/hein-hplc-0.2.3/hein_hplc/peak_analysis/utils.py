import pandas as pd
import rainbow as rb


def read_uv(filename):
    data_uv = rb.agilent.chemstation.parse_file(filename)
    df_rt = pd.DataFrame({"RT (min)": data_uv.xlabels})
    df_ab = pd.DataFrame(data_uv.data, columns=data_uv.ylabels)
    df = pd.concat([df_rt, df_ab], axis=1)
    return df


if __name__ == "__main__":
    df = read_uv(r"C:\Users\User\Desktop\test_hplc_dir\004-4-mixture2.D\DAD1.UV")
    print(df.head())

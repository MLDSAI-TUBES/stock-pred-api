# if __name__ == "__main__":
print('hello')
import preprocess
import normalize_features

p = preprocess.PreprocessIndependentVariables('TLKM.JK')
df = p.getDF()
print(df)

nf = normalize_features.NormalizeFeatures(df)
df_scaled = nf.getScaledDF()

print(df_scaled)
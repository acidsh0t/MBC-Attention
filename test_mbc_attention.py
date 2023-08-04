from tools.MultiBranchCNN import *
from tensorflow import keras
import os

def predictSequenceFromSaveKerasMdl(test_path, mdl_path, testRs_path, ft_list=def_fts):
    test_fastas, test_fastas_file = geneFastasFromFastaFile(test_path)
    fastas = pd.read_csv(test_fastas_file)
    sets = CNNimportFtsDataSetsPoNe(fastas, ft_list=ft_list, target=None)
    names, seqs, lens, records = readFastaYan(test_path)
    X, Y = CNNstandardInputOutput(sets)
    mdl_name = os.path.basename(mdl_path)
    CNNMdl = keras.models.load_model(mdl_path)
    pred = CNNMdl.predict(X)
    pred = pred / def_scale - def_bias
    fastas["Prediction"] = 10 ** (-pred)
    fastas.to_csv(testRs_path, index=False)
    print("save %s prediction to: %s" % (test_path, testRs_path))
    return pred

fasta=[]

if __name__ == "__main__":
    for file in os.listdir():
        if file.endswith('.fasta'):
            fasta.append(file)
    for i in fasta:
        name=i.replace('.fasta','')
        # generate test features
        test_path = i
        mdl_path = 'model/whole_train.mdl'
        predict_test_path = name+'.csv'
        pred = predictSequenceFromSaveKerasMdl(test_path, mdl_path, predict_test_path)
        

import json
import matplotlib.pyplot as plt
import numpy as np

def loadJson(filePath:str):
    with open(filePath, 'r') as f:
        jsonDict = json.load(f)
    return jsonDict

def makeMasterFile():
    rescale100File = "API_Project/AWS-Rescale100x100-Labels/All-100x100-Labels.json"
    rescale80File = "API_Project/AWS-Rescale80x80-Labels/All-80x80-Labels.json"
    rescale40File = "API_Project/AWS-Rescale40x40-Labels/All-40x40-Labels.json"
    svmAndActualFile = "svmAndActual.json"

    rescale100Labels = loadJson(rescale100File)
    rescale80Labels = loadJson(rescale80File)
    rescale40Labels = loadJson(rescale40File)
    svmAndActualLabels = loadJson(svmAndActualFile)

    imgNames = list(svmAndActualLabels.keys())
    keyNames = ["actual", "aws-100x100", "aws-80x80", "aws-40x40", "svm"]

    data = dict()
    
    for img in imgNames:
        data[img] = {
            keyNames[0]: svmAndActualLabels[img]["Actual"],
            keyNames[1]: rescale100Labels[img],
            keyNames[2]: rescale80Labels[img],
            keyNames[3]: rescale40Labels[img],
            keyNames[4]: svmAndActualLabels[img]["Predicted"]
        }
    
    json_string = json.dumps(data, sort_keys=True, indent=4, 
        separators=(',',':'))
    
    with open("master-03-31-2019.json", "w") as f:
        f.write(json_string)

def getAccuracy(data, imgNames):
    genderData = dict()
    genderData["actual"] = {"male":0,"female":0}
    genderData["aws-100x100"] = {"male":0,"female":0}
    genderData["svm"] = {"male":0,"female":0}
    genderData["aws-80x80"] = {"male":0,"female":0}
    genderData["aws-40x40"] = {"male":0,"female":0}
    for img in imgNames:
        try:
            if data[img]["actual"] == 1:
                genderData["actual"]["male"] += 1
                if data[img]["aws-100x100"]["FaceDetails"][0]["Gender"]["Value"] == "Male":
                    genderData["aws-100x100"]["male"] += 1
                if (data[img]["aws-40x40"]["FaceDetails"][0]["Gender"]["Value"] == "Male" or
                    len(data[img]["aws-40x40"]["FaceDetails"]) == 0):
                    genderData["aws-40x40"]["male"] += 1
                if data[img]["aws-80x80"]["FaceDetails"][0]["Gender"]["Value"] == "Male":
                    genderData["aws-80x80"]["male"] += 1
                if data[img]["svm"] == 1:
                    genderData["svm"]["male"] += 1
            else:
                genderData["actual"]["female"] += 1
                if data[img]["aws-100x100"]["FaceDetails"][0]["Gender"]["Value"] == "Female":
                    genderData["aws-100x100"]["female"] += 1
                if (data[img]["aws-40x40"]["FaceDetails"][0]["Gender"]["Value"] == "Female" or
                    len(data[img]["aws-40x40"]["FaceDetails"]) == 0):
                    genderData["aws-40x40"]["female"] += 1
                if data[img]["aws-80x80"]["FaceDetails"][0]["Gender"]["Value"] == "Female":
                    genderData["aws-80x80"]["female"] += 1
                if data[img]["svm"] == 0:
                    genderData["svm"]["female"] += 1
        except:
            pass

    return genderData

def plotGenderData(genderData):
    print(genderData)
    keys = list(genderData.keys())
    keys.remove("actual")
    males = []
    females = []
    for key in keys:
        males.append(genderData[key]["male"]/genderData["actual"]["male"]*100)
        females.append(genderData[key]["female"]/genderData["actual"]["female"]*100)
    print(males)
    print(females)
    data = [males,females]

    barWidth = 0.25
    r1 = np.arange(len(males))
    r2 = [x + barWidth for x in r1]
    
    plt.bar(r1, males, color='c', width=barWidth, edgecolor='white', 
        label='Males')
    plt.bar(r2, females, color='m', width=barWidth, edgecolor='white', 
        label='Females')
    
    plt.xticks([r + barWidth/2 for r in range(len(keys))], ["CNN-100x100","SVM-100x100","CNN-80x80","CNN-40x40"])
    plt.ylim(0,100)
    plt.ylabel("Accuracy (%)")
    plt.grid(alpha = 200)
    plt.title("Comparing Accuracies between CNN and SVM")
    plt.legend()
    plt.show()
    
def getConfidences(data, imgNames):
    age = dict({"aws-100x100":[], "aws-80x80":[], "aws-40x40":[]})
    gender = dict({"aws-100x100":[], "aws-80x80":[], "aws-40x40":[]})

    for img in imgNames:
        for key in list(age.keys()):
            try:
                gender[key].append(data[img][key]["FaceDetails"][0]["Gender"]["Confidence"])
                ageHigh = data[img][key]["FaceDetails"][0]["AgeRange"]["High"]
                ageLow = data[img][key]["FaceDetails"][0]["AgeRange"]["Low"]
                age[key].append(ageHigh - ageLow)
            except:
                pass
    keys = list(age.keys())
    avgConfidence = []
    avgAgeRange = []
    for key in keys:
        avgConfidence.append(sum(gender[key])/len(gender[key]))
        avgAgeRange.append(sum(age[key])/len(age[key]))

    plt.bar(keys, avgConfidence, color = 'm')
    plt.ylabel("Confidence (%)")
    plt.ylim(0,100)
    plt.xlabel("Picture Resolution")
    plt.xticks([0,1,2],["100x100", "80x80", "40x40"])
    plt.title("Gender Prediction Confidence using a CNN")
    plt.show()

    plt.bar(keys, avgAgeRange, color = 'm')
    plt.ylabel("Predicted Age Range")
    plt.xlabel("Picture Resolution")
    plt.xticks([0,1,2],["100x100", "80x80", "40x40"])
    plt.title("Age Prediction Range")
    plt.show()

def main():
    masterFile = "master-03-31-2019.json"
    data = loadJson(masterFile)
    imgNames = list(data.keys())

    # keyNames = ["actual", "aws-100x100", "aws-40x40", "aws-80x80", "svm"]
    # print(data[imgNames[0]]["aws-100x100"]["FaceDetails"])
    plotGenderData(getAccuracy(data, imgNames))
    getConfidences(data, imgNames)

main()
# makeMasterFile()
import preprocess
import model_loader
def model_predict(img_path, models=None):
    DIMS = (224, 224, 3)
    DIMS_CONV = (300, 300, 3)

    img_tensor = preprocess.preprocess_img(img_path, DIMS)
    img_tensor_conv = preprocess.preprocess_img(img_path, DIMS_CONV)
    img_tensor_flat = img_tensor.reshape((1, -1))
    res = {
        "transfer_learning": {},
        "hybrid_learning": {},
        "sequential_learning": {},
        "machine_learning": {}
    }
    
    if models is None:
        models = model_loader.get_models(transfer_learning=False, hybrid=False, sequential=False)
    
    res["sequential_learning"]["CONV2D"] = "{:.3f}".format(models["sequential"]["CONV2D"].predict(img_tensor_conv)[0][0])

    for model_name, model in models["transfer_learning"].items():
        res["transfer_learning"][model_name] = "{:.3f}".format(model.predict(img_tensor)[0][0])

    # res["transfer_learning"]["VGG19"] = "{:.3f}".format(models["transfer_learning"]["VGG19"].predict(img_tensor)[0][0])
    # res["MobileNet V2"] = "{:.3f}".format(model_mobv2.predict(img_tensor)[0][0])
    # # res["ResNet 50"] = str(model_resnet50.predict(img_tensor)[0][0])
    # res["Inception V3"] = "{:.3f}".format(model_incepv3.predict(img_tensor)[0][0])

    vgg_features_output = models["hybrid_models"]["VGG19_Features"].predict(img_tensor);
    res["hybrid_learning"]["VGG19 + SVM"] = "{:.3f}".format(models["hybrid_models"]["SVM"].predict_proba(vgg_features_output)[0][1])
    # print(res["VGG19 + SVM"])
    res["hybrid_learning"]["VGG19 + RF"] = "{:.3f}".format(models["hybrid_models"]["RF"].predict(vgg_features_output)[0])
    

    res["machine_learning"]["SVM"] = "{:.3f}".format(models["machine_learning"]["SVM"].predict(img_tensor_flat)[0])
    res["machine_learning"]["Logistic Regression"] = "{:.3f}".format(models["machine_learning"]["LR"].predict(img_tensor_flat)[0])
    res["machine_learning"]["KNN"] = "{:.3f}".format(models["machine_learning"]["KNN"].predict(img_tensor_flat)[0])
    res["machine_learning"]["Random Forest"] = "{:.3f}".format(models["machine_learning"]["RF"].predict(img_tensor_flat)[0])
    res["machine_learning"]["Naive Bayes"] = "{:.3f}".format(models["machine_learning"]["NB"].predict(img_tensor_flat)[0])
    
    # except Exception as e:
    #     print(e)
    # # if preds[0][0] > 0.5:
    #     return "Lyme - Positive"
    # else:
    #     return "Lyme - Negative"
    return res

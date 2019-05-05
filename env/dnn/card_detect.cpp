//
// Created by holaverse on 19-4-29.
//

#include "card_detect.h"

CardDetect::CardDetect() {
    this->load_dict();
    string mode_path = "./asset/card_net.pb";
    this->load_model(mode_path);
}


bool CardDetect::load_model(string mode_path) {
    this->net = cv::dnn::readNetFromTensorflow(mode_path);
    if (this->net.empty()) {
        cout << "Card net load fail." << endl;
    } else {
        cout << "Card net load success." << endl;
    }
}

CardResult CardDetect::predict(Mat &src) {
    Mat inputBlob = cv::dnn::blobFromImage(src, 1. / 255, Size(96, 96), cv::Scalar(), false, false);
    net.setInput(inputBlob, "input");//set the network input, "data" is the name of the input layer

    vector<cv::String> blobNames;
    blobNames.emplace_back("card_net/type_pred");
    blobNames.emplace_back("card_net/available_pred");

    vector<Mat> outputs;
    net.forward(outputs, blobNames);
    int type = argmax(outputs[0]);
    int available = argmax(outputs[1]);
    CardResult result;
    result.card_type = type;
    result.available = available;
    result.card_name = this->char_dict[to_string(type).data()].GetString();
    result.prob = ((float *) outputs[0].data)[type];
    return result;
}

int CardDetect::argmax(Mat &src) {
    auto *data = (float *) src.data;
    int max_index = 0;
    float max_value = -99;
    for (int c = 0; c < src.cols; c++) {
        if (data[c] > max_value) {
            max_index = c;
            max_value = data[c];
        }
    }
    return max_index;
}

void CardDetect::load_dict() {
    this->char_dict.Parse(this->card_dict_json);

    if (debug) {
        rapidjson::StringBuffer buffer;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
        this->char_dict.Accept(writer);

        std::cout << buffer.GetString() << std::endl;
    }
}

void CardDetect::reset() {
    pre_type[0] = 0;
    pre_type[1] = 0;
    pre_type[2] = 0;
    pre_type[3] = 0;
}




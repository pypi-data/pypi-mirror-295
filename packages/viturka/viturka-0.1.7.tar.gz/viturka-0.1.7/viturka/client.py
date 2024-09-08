import requests
import pickle
import base64

class ModelUploader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.server_url = "https://viturka.com/upload_model"

    def upload_model(self, local_model, model_type):
        # Serialize the local model
        model_data = pickle.dumps(local_model)

        # Send the model to the server and receive the global model
        response = requests.post(
            f'{self.server_url}',
            files={'model': ('model.pkl', model_data)},
            data={'api_key': self.api_key, 'model_type': model_type}
        )


        if response.status_code == 200:
            # Deserialize the received global model
            data = response.json()
            #print(data)
            if data['model'] == 200:
                global_model = local_model
            else:

                # Decode the base64 encoded string back to bytes

                pickled_model = base64.b64decode(data['model'])

                # Unpickle the model
                global_model = pickle.loads(pickled_model)

            # Perform local aggregation
                local_model.w0_ += global_model.w0_

                # Resize and perform element-wise aggregation for w_ and V_ parameters
                if len(local_model.w_) != len(global_model.w_):
                    min_len = min(len(local_model.w_), len(global_model.w_))
                    local_model.w_[:min_len] += global_model.w_[:min_len]
                    global_model_extra_w = global_model.w_[min_len:] if len(global_model.w_) > min_len else []
                    local_model_extra_w = local_model.w_[min_len:] if len(local_model.w_) > min_len else []
                    local_model.w_ = np.concatenate([local_model.w_[:min_len] / 2, global_model_extra_w, local_model_extra_w])
                else:
                    local_model.w_ += global_model.w_
                    local_model.w_ /= 2

                if len(local_model.V_) != len(global_model.V_):
                    min_len = min(len(local_model.V_), len(global_model.V_))
                    local_model.V_[:min_len] += global_model.V_[:min_len]
                    global_model_extra_V = global_model.V_[min_len:] if len(global_model.V_) > min_len else []
                    local_model_extra_V = local_model.V_[min_len:] if len(local_model.V_) > min_len else []
                    local_model.V_ = np.concatenate([local_model.V_[:min_len] / 2, global_model_extra_V, local_model_extra_V])
                else:
                    local_model.V_ += global_model.V_
                    local_model.V_ /= 2
            print("Model uploaded and aggregated successfully.")
        else:
            print(f"Failed to upload model: {response.content.decode()}")

        return local_model


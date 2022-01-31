import axios from "axios";
const baseUrl = "http://f457-34-86-42-205.ngrok.io";

const requestToServer = async (req) => {
  const params = new URLSearchParams();
  params.append("x", req.x);
  params.append("y", req.y);
  params.append("w", req.w);
  params.append("h", req.h);
  params.append("image", req.image);
  const token = "24Gj4z8JODNMriG0cCB9NfWTRzg_3zzBeRVQnynadewEHQDaG";
  const config = {
    headers: { Authorization: `Bearer ${token}` },
  };

  const response = await axios.post(baseUrl, params, config);

  return response;
};

export default requestToServer;

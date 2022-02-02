import axios from "axios";
const baseUrl = "http://d3d0-35-194-176-182.ngrok.io";

const requestToServer = async (req) => {
  const params = new URLSearchParams();
  params.append("x", req.x);
  params.append("y", req.y);
  params.append("x_max", req.x_max);
  params.append("y_max", req.y_max);
  params.append("image", req.image);
  const token = "24Gj4z8JODNMriG0cCB9NfWTRzg_3zzBeRVQnynadewEHQDaG";
  const config = {
    headers: { Authorization: `Bearer ${token}` },
  };

  const response = await axios.post(baseUrl, params);

  return response;
};

export default requestToServer;
import axios from "axios";
const baseUrl = "https://ise-backend-jd981.loca.lt/";

const requestToServer = async (req) => {
  const params = new URLSearchParams();
  params.append("x", req.x);
  params.append("y", req.y);
  params.append("x_max", req.x_max);
  params.append("y_max", req.y_max);
  params.append("image", req.image);
  params.append("method", req.method);

  const response = await axios.post(baseUrl, params);

  return response;
};

export default requestToServer;
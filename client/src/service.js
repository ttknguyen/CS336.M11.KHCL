import axios from "axios";

const requestToServer = async (req, baseUrl) => {
  const params = new URLSearchParams();
  params.append("x", req.x);
  params.append("y", req.y);
  params.append("x_max", req.x_max);
  params.append("y_max", req.y_max);
  params.append("image", req.image);
  params.append("method", req.method);

  const timeoutRequest = { timeout: 600000 };

  const response = await axios.post(baseUrl, params, timeoutRequest);
  return response;
};

const checkHeathApi = async (baseUrl) => {
  try {
    const response = await axios.get(baseUrl);
    return true;
  } catch (error) {
    return false;
  }
};

const services = {
  requestToServer,
  checkHeathApi,
};

export default services;
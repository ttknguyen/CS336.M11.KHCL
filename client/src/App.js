import logo from "./logo.svg";
import "./App.css";
import React, { useState, useEffect, useRef } from "react";
import { Form, Button, Container, Image } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import ReactCrop from "react-image-crop";
import "react-image-crop/dist/ReactCrop.css";
import services from "./service";
import background from "./assets/background.png";

function App() {
  const [srcImg, setSrcImg] = useState(null);
  const [image, setImage] = useState(null);
  const [crop, setCrop] = useState({});
  const [queryPath, setQueryPath] = useState("");
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [method, setMethod] = useState("");
  const [apiHealth, setApiHealth] = useState(false);
  const [apiUrl, setApiUrl] = useState("");

  useEffect(() => {
    document.title = "Image search engine";
  }, []);

  const handleImage = async (event) => {
    if (event.target.files[0].type.match("image/*") === null) {
      return setError("Image file is required");
    } else {
      setError("");
    }
    setSrcImg(URL.createObjectURL(event.target.files[0]));
  };

  const handleMethod = async (event) => {
    const id = event.target.id;
    return setMethod(id.charAt(id.length - 1) - 1);
  };

  const handleApiUrl = async (event) => {
    await setApiUrl(event.target.value);
  };

  const handleSubmitUrl = async () => {
    const check = await services.checkHeathApi(apiUrl);
    if (check) {
      await setApiHealth(true);
      await setError("");
    } else {
      await setError("API not found");
    }
  };

  const handleSubmit = async () => {
    if (method === "") return setError("Please choose a method");
    else setError("");

    if (!image) return setError("Please upload a file");
    else setError("");

    await setLoading(true);
    const canvas = document.createElement("canvas");
    canvas.width = image.width;
    canvas.height = image.height;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(image, 0, 0, image.width, image.height);
    const base64Image = canvas.toDataURL("image/png", 1);

    const req = {
      x: crop.x,
      y: crop.y,
      x_max: crop.x + crop.width,
      y_max: crop.y + crop.height,
      image: base64Image,
      method,
    };

    await console.log(req);

    const response = await services.requestToServer(req, apiUrl);
    // await setQueryPath(response.data["query-path"]);
    await setResult(response.data.results);
    await setLoading(false);
  };

  const listResult = result.map((base64Img) => {
    return (
      <li key={base64Img}>
        <img
          src={`data:image/png;base64,${base64Img}`}
          alt="Loading..."
          class="img-thumbnail"
        />
      </li>
    );
  });

  return apiHealth ? (
    <div style={{ backgroundImage: `url(${background})`, backgroundSize: 'cover', backgroundRepeat: 'no-repeat',
                  backgroundPosition: 'center', marginTop:'-17px', height: '100vh' }}>
    <Container className="container" fluid="md">
      <h1 className="d-flex justify-content-center"><b>IMAGE SEARCH ENGINE</b></h1>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label className="d-flex justify-content-center">
            <b>Select Image you want to retrieve</b>
          </Form.Label>
          {error && (
            <Form.Label className="d-flex justify-content-center text-danger">
              {error}
            </Form.Label>
          )}

          <div className="mb-3 d-flex justify-content-center">
            <input
              class="form-control"
              type="file"
              id="formFile"
              accept=".jpg, .jpeg, .png"
              onChange={handleImage}
            />
          </div>

          <div>
            {srcImg && (
              <div id="inputImg" className="d-flex justify-content-center">
                <ReactCrop
                  style={{ maxWidth: "75%" }}
                  src={srcImg}
                  onImageLoaded={setImage}
                  crop={crop}
                  onChange={setCrop}
                />
              </div>
            )}
          </div>
          <Form.Label className="d-flex justify-content-center">
            <b>Select method for Search Engine</b>
          </Form.Label>
          <div
            class="btn-group"
            role="group"
            aria-label="Basic radio toggle button group"
            className="d-flex justify-content-center mt-3"
            onChange={handleMethod}
          >
            <input
              type="radio"
              class="btn-check"
              name="btnradio"
              id="btnradio1"
              autocomplete="off"
            />
            <label class="btn btn-outline-primary" for="btnradio1" 
                  style={{padding: '1.1em 4em',
                          borderRadius: '10px',
                        }}>
              <b>SIR</b>
            </label>

            <input
              type="radio"
              class="btn-check"
              name="btnradio"
              id="btnradio2"
              autocomplete="off"
            />
            <label class="btn btn-outline-primary" for="btnradio2"
                  style={{padding: '1.1em 2em',
                          borderRadius: '10px',
                        }}>
              <b>CNN-IRwNHA</b>
            </label>

            <input
              type="radio"
              class="btn-check"
              name="btnradio"
              id="btnradio3"
              autocomplete="off"
            />
            <label class="btn btn-outline-primary" for="btnradio3"
                  style={{padding: '1.1em 3.7em',
                          borderRadius: '10px',
                        }}>
              <b>DELF</b>
            </label>
          </div>
        </Form.Group>
        <div class="d-flex justify-content-center">
          <Button variant="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </div>
      </Form>
      {loading && (
        <div class="d-flex justify-content-center mt-3">
          <div class="spinner-grow text-primary" role="status">
            <span class="sr-only"></span>
          </div>
          <div class="spinner-grow text-secondary" role="status">
            <span class="sr-only"></span>
          </div>
          <div class="spinner-grow text-success" role="status">
            <span class="sr-only"></span>
          </div>
          <div class="spinner-grow text-danger" role="status">
            <span class="sr-only"></span>
          </div>
          <div class="spinner-grow text-warning" role="status">
            <span class="sr-only"></span>
          </div>
          <div class="spinner-grow text-info" role="status">
            <span class="sr-only"></span>
          </div>
        </div>
      )}
      <ul>{listResult}</ul>
    </Container>
    </div>
   ) : (
    <div style={{ backgroundImage: `url(${background})`, backgroundSize: 'cover', backgroundRepeat: 'no-repeat',
                  backgroundPosition: 'center', marginTop:'-17px', height: '100vh' }}>
    <Container className="container" fluid="md">
      <h1 className="d-flex justify-content-center"><b>IMAGE SEARCH ENGINE</b></h1>
      <Form.Label className="d-flex justify-content-center">
        <b>Input API URL</b>
      </Form.Label>
      {error && (
        <Form.Label className="d-flex justify-content-center text-danger">
          {error}
        </Form.Label>
      )}
      <div className="mb-3 d-flex justify-content-center">
        <input class="form-control" type="url" onChange={handleApiUrl} />
      </div>
      <div class="d-flex justify-content-center">
        <Button variant="primary" onClick={handleSubmitUrl}>
          Submit
        </Button>
      </div>
    </Container>
    </div>
  );
}

export default App;
import axios from 'axios';

import React, { Component, useState } from 'react';

function App() {

  const [selectedFile, onSelectedFile] = useState(null);
  const onFileChange = event => {
    onSelectedFile(event.target.files[0])
  };

  const onFileUpload = () => {

    var axios = require('axios');
    const formData = new FormData();
    formData.append(
      "Image",
      selectedFile,
    );
    if (selectedFile.type === "image/png" || selectedFile === "image/jpg" || selectedFile === "image/jpeg") {
      var config = {
        method: 'post',
        url: 'http://127.0.0.1:5000/predict',
        data: formData
      };

      axios(config)
        .then(function (response) {
          const result = response.data.message[0]
          if (result[0] > result[1]) {
            alert("Results are negative. Patient doesn't have lung cancer")
          }
          else if (result[0] < result[1]) {
            alert("Results are postive. Patient unfortunately has lung cancer")
          }
          else if (result[0] === result[1]) {
            alert("Results are unclear. Further testing required.")
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    }
    else {
      alert("Wrong file type selected. Only supported types are jpg, jpeg, and png")
    }
  };


  return (
    <div>
      <h1>
        Lung Cancer Detection
      </h1>
      <div>
        <input type="file" onChange={onFileChange} />
        <button onClick={onFileUpload}>
          Upload!
        </button>
      </div>
    </div>
  );
}

export default App;

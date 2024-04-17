import React, { Component } from 'react';
import './App.css';
import FileDropper from './components/FileDropper/FileDropper.js';
import axios from 'axios';
import { ClapSpinner } from "react-spinners-kit";

const initialState = {
  selectedFile: null,
  upscaleLevel: 4,
  imageBefore: null,
  loaded: 0,
  loading: false,
  imgAfter: null,
}

class App extends Component {
  constructor() {
    super();
    this.state = initialState;
  }

  onChangeHandler = event => {
    this.setState({
      selectedFile: event.target.files[0],
      loaded: 0,
    })
    if (event.target.files[0] != null) {
      this.setState({
        imageBefore: URL.createObjectURL(event.target.files[0]),
      })
    }

  }


  onSelectUpscaleLevelHandler = e =>{
    this.setState({
      upscaleLevel: e.target.value
    })
  }

  onClickHandler = () => {
    if (this.state.imageBefore != null) {
      this.setState({
        loading: true,
      });

      const data = new FormData()
      data.append('file', this.state.selectedFile)
      data.append('upscale_level', this.state.upscaleLevel)
      axios.post("http://localhost:5000/api/upload",
        data,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      ).then(res => {
        this.setState({
          loading: false,
          imgAfter: res.data
        });
      }).catch(e => {
        this.setState({
          loading: false,
        })
        console.log('errrrrrr',e);
      })
    }
  }

  render() {
    return (
      <div className="App">
        <FileDropper 
          onChangeHandler={this.onChangeHandler} 
          onClickHandler={this.onClickHandler} 
          onSelectUpscaleLevelHandler={this.onSelectUpscaleLevelHandler}
          upscaleLevel={this.state.upscaleLevel}
        />
        <div id="inner">
          <ClapSpinner
            loading={this.state.loading}
            size={50}
          />
        </div>
        <div className="column">
          {this.state.imageBefore == null ? "" : <img width="90%" src={this.state.imageBefore} alt="before" />}
        </div>
        {this.state.imgAfter == null ? "" :
          <div className="column">
            <a href={this.state.imgAfter} download>
              Click on image to download
              <img width="90%" src={this.state.imgAfter} alt="after" />
            </a>
          </div>
        }
      </div>
    );
  }
}

export default App;

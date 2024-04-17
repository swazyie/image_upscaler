import React from 'react';
import './FileDropper.css';
const FileDropper = ({ onChangeHandler, onClickHandler, onSelectUpscaleLevelHandler, upscaleLevel }) => {

    return (
        <div className="container">
            <div className="row">
                <div className="offset-md-3 col-md-6">
                    <div className="form-group files">
                        <label><b>Upload Your File to be Upscaled (with <a href="https://github.com/xinntao/ESRGAN">ESRGAN</a>)</b></label>
                        <input type="file" className="form-control" multiple onChange={onChangeHandler} />
                    </div>
                    <div className="form-group">


                    </div>

                    <button type="button" className="btn btn-success btn-block" onClick={onClickHandler}>Upscale</button>
                    <select name="Upscale Level" id="upscale" onChange={onSelectUpscaleLevelHandler} value={upscaleLevel} >
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        {/* <p>{upscaleLevel}</p> */}
                    </select>

                </div>
            </div>
        </div>
    );


}
export default FileDropper;
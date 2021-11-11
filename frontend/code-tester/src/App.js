import React from 'react';
import './App.css';
import $ from 'jquery';
import ENVS from './env';
import ROUTES from './routes';

class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {env:ENVS.DEV, report: {}, link:'#'};
    this.handle_gene_rdm_objects = this.handle_gene_rdm_objects.bind(this);
    this.handle_report_rdm_objects = this.handle_report_rdm_objects.bind(this);
  }

  handle_gene_rdm_objects(){
    $.ajax({
      url: this.state.env + ROUTES.GENE_RDM_OBJECT_LINK,
      method: 'GET',
      success: function(result) {
        result = JSON.parse(result);
        if(result.code === 200){
          this.setState({link: result.data});
        }else{
          alert(result.message);
        }
          
      }.bind(this),
      error: function(err){
        alert(err);
      }
    });
  }

  handle_report_rdm_objects(){
    if(this.state.link !== "#"){
      let filename_param = this.state.link.split('?')[1];
      $.ajax({
        url:  this.state.env + ROUTES.REPORT_RDM_OBJECT_LINK + '?' + filename_param,
        method: 'GET',
        success: function(result) {
          result = JSON.parse(result);
          console.log(result);
          if(result.code === 200){
            this.setState({report: result.data});
          }else{
            alert(result.message);
          }
            
        }.bind(this),
        error: function(err){
          alert(err);
        }
      });
    } else {
      alert("Oops, unable to find objects report");
    }
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
        <h2>Coding Challenge</h2>
        <hr />
        <button onClick={this.handle_gene_rdm_objects}>Generate</button>
        <h5>Download link: <a href={this.state.link} target="_blank">{this.state.link}</a></h5>
        <button onClick={this.handle_report_rdm_objects}>Report</button>
        <div>
          <p> Alphabet: {this.state.report.alpha}        
            </p>
        </div>
        <div>
          <p> AlphabetNumeric: {this.state.report.alpha_num}        
            </p>
        </div>
        <div>
          <p> Integar: {this.state.report.integar}        
            </p>
        </div>
        <div>
          <p> RealNumber: {this.state.report.real_num}        
            </p>
        </div>
        </header>
      </div>
    );
  }
}

export default App;

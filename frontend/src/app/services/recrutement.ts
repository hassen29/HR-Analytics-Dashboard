import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class Recrutement {


  url = 'http://127.0.0.1:8000/api/'
  constructor(private http:HttpClient){


  }

  predictjob (fonction : any){

    return this.http.post (this.url + 'predict', fonction)
  }

  getcandidat (){

    return this.http.get(this.url + 'candidates');
  }
  


  predictAndAdd(formData: FormData) {
  return this.http.post(this.url + 'predict/', formData);
}


  getpredictions (){

    return this.http.get(this.url + 'predictions');
  }
  

}

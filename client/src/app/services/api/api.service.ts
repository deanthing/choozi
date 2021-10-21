import { HttpClient } from '@angular/common/http';
import { ValueTransformer } from '@angular/compiler/src/util';
import { Injectable, ɵresetJitOptions } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  URL_BASE: string = 'http://127.0.0.1:8000/';

  callRes?: any;

  constructor(private http: HttpClient) {}

  getData(endpoint: string, param?: any) {
    var getUrl = '';
    if (param) {
      getUrl = this.URL_BASE + endpoint + '/' + param;
    } else {
      getUrl = this.URL_BASE + endpoint;
    }
    return this.http.get<any>(getUrl, {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      responseType: 'json',
    });
  }

  deleteData(endpoint: string, param?: any) {
    var getUrl = '';
    if (param) {
      getUrl = this.URL_BASE + endpoint + '/' + param;
    } else {
      getUrl = this.URL_BASE + endpoint;
    }
    return this.http.delete<any>(getUrl, {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      responseType: 'json',
    });
  }

  postData<T>(endpoint: string, data: any) {
    return this.http.post<T>(this.URL_BASE + endpoint, data, {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
}

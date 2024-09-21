import { Component, OnInit, ElementRef, ViewChild, ViewChildren, QueryList, Input } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

/*
export class AppComponent {
  title = "Runners Web";
}
*/


export class AppComponent implements OnInit {

  
  constructor (private http: HttpClient) {

  }

  title = "Runners Web";

  API = environment.api; 

  year= (new Date()).getFullYear();

  meetwaarden: any = [];
  totalen: any = [];

  date = (new Date()).toISOString().substring(0,10)
  minutes = "0";

  ngOnInit() {
    this.getMeetwaarden();  
  }

  getMeetwaarden() {
    this.http.get(`${this.API}/meetwaarde?year=${this.year}`)
      .subscribe(meetwaarden => {
        this.meetwaarden = meetwaarden;
      });
    this.http.get(`${this.API}/totaal?year=${this.year}`)
      .subscribe(totalen => {
        this.totalen = totalen;
      });
  }

  @ViewChild('scrollList') private scrollList!: ElementRef;

  scrollToBottom() {
    let element = this.scrollList.nativeElement;
    element.scrollTop = element.scrollHeight;
  }


  @ViewChildren('scrollList') private scrollChildren!: QueryList<Object>;

  ngAfterViewInit() {
    this.scrollChildren.changes.subscribe(t => {
      this.scrollToBottom();
    })
  }

  plusYear() {
    this.year++;
    this.getMeetwaarden();
  }

  minYear() {
    this.year--;
    this.getMeetwaarden();
  }

  addMeetwaarde() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    this.http.post(`${this.API}/meetwaarde`, 
      { date: this.date, minutes: this.minutes}, 
      httpOptions
    ).subscribe(res => {
        this.getMeetwaarden();
        this.date = (new Date()).toISOString().substring(0,10);
        this.minutes = "0";
      }
    );
  }

  deleteMeetwaarde(date: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: {date: date}
    };
    this.http.delete(`${this.API}/meetwaarde`, 
      httpOptions
    ).subscribe((v) => {
        this.getMeetwaarden();
      }
    );
  }
}


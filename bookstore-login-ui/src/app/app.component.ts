import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ConfigService } from '../util/config.service';
import { ActivatedRoute } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  //Note: this component is using standalone, for ngModules just import on module providers
  configService = inject(ConfigService);
  name: string | null = null;
  token: string | null = null;
  role: string | null = null;
 books: any[] = []; 
  apiUrl = this.configService.readConfig().API_URL;
  showCart = false;


  constructor(private route: ActivatedRoute,private http: HttpClient) {
    console.log(this.configService.readConfig().API_URL);
  }

   ngOnInit(): void {

    debugger;
    // Read 'name' from query parameters
    this.route.queryParams.subscribe(params => {
      this.name = params['name'] || null;
      this.token=params['token'] || null;
      this.role=params['role'] || null;

      if (this.token) {
        this.loadBooks();
      }

    });
  }

  loadBooks() {
    const headers = new HttpHeaders({
      "Authorization": `Bearer ${this.token}`
    });

    this.http.get<any[]>("http://localhost:8000/api/book/details", { headers })
      .subscribe({
        next: (data) => this.books = data,
        error: (err) => console.error("API Error:", err)
      });
  }

  loginWithGoogle() {
    // Redirect to your backend endpoint which handles Google OAuth
    window.location.href = 'http://localhost:8001/auth/login';
  }

  cartCount = 0;
  addedBooks: any[] = [];
  allAddedBooks: any[] = [];

  selectedBook: any = null;   // only one object

   addToCart(book: any) {
      this.allAddedBooks.push(book);
      this.addedBooks.push(book.book_id);   // store only ID
      this.selectedBook = book;   // save the current selection
      this.cartCount++; 
  }

  toggleCart() {
  this.showCart = !this.showCart;
}

buyBooks() {
  alert("Purchase successful!");

  this.allAddedBooks = [];
  this.addedBooks = [];
  this.cartCount = 0;
  this.showCart = false;
}


}

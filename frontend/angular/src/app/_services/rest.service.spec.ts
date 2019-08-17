import { TestBed, async } from '@angular/core/testing';
import { RestService } from './rest.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';


describe('RestService', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
    })
    .compileComponents();
  }));

  it('should be created', () => {
    const service: RestService = TestBed.get(RestService);
    expect(service).toBeTruthy();
  });
});

import { Body, Controller, Get, Post } from '@nestjs/common';
import { AppService } from './app.service';
import { Job } from './Jobs/Job';

@Controller("/")
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post("/jobs")
  public createJob(@Body() job: Job) {
    return this.appService.createJob(job);
  }
}

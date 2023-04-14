import { AMQPService } from '@nestjs.pro/amqp';
import { Injectable } from '@nestjs/common';
import { Job } from './Jobs/Job';

@Injectable()
export class AppService {
    public constructor(private readonly amqpService: AMQPService) {
    }
    public createJob(job: Job): void {
        this.amqpService.getConnection().subscribe(connection => {
            connection.reference.channel.publish(
                'lisa',
                'jobs.new',
                Buffer.from(JSON.stringify(job))
            );
        });
    }
}

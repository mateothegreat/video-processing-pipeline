import { AMQPModule } from '@nestjs.pro/amqp/AMQPModule';
import { AMQPLogLevel } from '@nestjs.pro/amqp/logging/AMQPLogLevel';
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
    imports: [
        AMQPModule.forRoot({
            logLevel: AMQPLogLevel.ERROR,
            autoConnect: true,
            connections: [
                {
                    name: 'default',
                    url: 'amqp://rabbitmq:agaeq14@localhost:5672',
                    exchange: {
                        name: 'lisa',
                        type: 'topic',
                        options: {
                            durable: true
                        }
                    },
                    queues: [
                        {
                            name: 'jobs.new',
                            routingKey: 'jobs.new',
                            createBindings: true,
                            options: {
                                durable: true
                            }
                        }
                    ]
                }
            ]
        })
    ],
    controllers: [ AppController ],
    providers: [ AppService ]
})
export class AppModule {
}

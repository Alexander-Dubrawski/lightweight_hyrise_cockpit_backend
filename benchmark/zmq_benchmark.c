//Compile with gcc -Wall -g zmq_benchmark.c -lzmq -std=c99 -lm -Werror -pthread -o benchmark
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#include <zmq.h>
#include <math.h>
#include <inttypes.h>

int RUNS = 10;
int CLIENTS = 2;

struct client_struct { 
   double latency[10000]; 
   double runtime;
   int runs;
   double throughput;
   double max_latency;
   double avg_latency;
   double std_latency;
   double req_sec;
}; 

double calculateSD(double mean, double data[]) {
    double SD = 0.0;
    for (int i = 0; i < RUNS; ++i)
        SD += pow(data[i] - mean, 2);
    return sqrt(SD / RUNS);
}

double get_mean(double data[]){
    double sum = 0.0;
    double mean = 0.0;
    for (int i = 0; i < RUNS; ++i) {
        sum += data[i];
    }
    mean = sum / RUNS;
    return mean;
}

double get_max(double data[]){
    double max = 0; 
    for (int i = 0; i < RUNS; ++i) {
        if (data[i] > max){
            max = data[i];
        }
    }
    return max;
}

void* zmq_runner(void* arg)
{
    struct client_struct *arg_struct = (struct client_struct*) arg;
    struct timespec requestStart, requestEnd;
    struct timespec benchmark_Start, benchmark_End;

    void *context = zmq_ctx_new ();
    void *requester = zmq_socket(context, ZMQ_REQ);
    zmq_connect (requester, "tcp://localhost:5555");

    clock_gettime(CLOCK_REALTIME, &benchmark_Start);
    for (int i = 0; i <= arg_struct->runs; i++) {
        char buffer [10];
        clock_gettime(CLOCK_REALTIME, &requestStart);
        zmq_send(requester, "Hello", 5, 0);
        zmq_recv(requester, buffer, 10, 0);
        clock_gettime(CLOCK_REALTIME, &requestEnd);
        //https://stackoverflow.com/questions/17705786/getting-negative-values-using-clock-gettime
        if ((requestEnd.tv_nsec-requestStart.tv_nsec)<0) {
                arg_struct->latency[i] = 1000000000 + requestEnd.tv_nsec-requestStart.tv_nsec;
        }
        else {
            arg_struct->latency[i] = (requestEnd.tv_nsec - requestStart.tv_nsec);
        }
    }
    clock_gettime(CLOCK_REALTIME, &benchmark_End);
    if ((benchmark_End.tv_nsec-benchmark_Start.tv_nsec)<0) {
        arg_struct->runtime = 1000000000 + benchmark_End.tv_nsec - benchmark_Start.tv_nsec;
    }
    else {
        arg_struct->runtime = (benchmark_End.tv_nsec - benchmark_Start.tv_nsec);
    }
    zmq_close (requester);
    zmq_ctx_destroy (context);
    arg_struct->max_latency = get_max(arg_struct->latency);
    arg_struct->avg_latency = get_mean(arg_struct->latency);
    arg_struct->std_latency = calculateSD(arg_struct->avg_latency, arg_struct->latency);
    arg_struct->throughput = arg_struct->runtime / RUNS;
    arg_struct->req_sec = 1.0 / (arg_struct->throughput / 1000000000);
    pthread_exit(0); 
}

int main(void){
    int runs = RUNS;
    int clients = CLIENTS;
    struct client_struct args[clients];
    pthread_t tids[clients];
    for (int i = 0; i < clients; i++) {
        args[i].runs = runs;
        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_create(&tids[i], &attr, zmq_runner, &args[i]);
    }
    double throughput = 0.0;
    double max_latency = 0.0;
    double avg_latency = 0.0;
    double std_latency = 0.0;
    double req_sec = 0.0;
    FILE *fptr;
    fptr = fopen("output.txt","w");
    fprintf(fptr,"[");
    for (int i = 0; i < clients; i++) {
        pthread_join(tids[i], NULL);
        printf("Runtime for thread %d is %lf\n",i, args[i].runtime);
        printf("throughput for thread %d is %lf\n",i, args[i].throughput);
        printf("max_latency for thread %d is %lf\n",i, args[i].max_latency);
        printf("avg_latency for thread %d is %lf\n",i, args[i].avg_latency);
        printf("std_latency for thread %d is %lf\n",i, args[i].std_latency);
        printf("req_sec for thread %d is %lf\n",i, args[i].req_sec);
        throughput += args[i].throughput;
        max_latency += args[i].max_latency;
        avg_latency += args[i].avg_latency;
        std_latency += args[i].std_latency;
        req_sec += args[i].req_sec;
        if (i == clients - 1){
            for (int z = 0; z < RUNS - 1; z++){
                fprintf(fptr,"%lf ,",args[i].latency[z]);
            }
            fprintf(fptr,"%lf",args[i].latency[RUNS-1]); 
        }
        else{
           for (int z = 0; z < RUNS; z++){
                fprintf(fptr,"%lf ,",args[i].latency[z]);
            }
        }
    }
    fprintf(fptr,"]");
    fclose(fptr);
    printf("\n\nthroughput is %lf\n", (throughput / CLIENTS));
    printf("max_latency is %lf\n", (max_latency / CLIENTS));
    printf("avg_latency is %lf\n", (avg_latency / CLIENTS));
    printf("std_latency is %lf\n", (std_latency / CLIENTS));
    printf("req_sec is %lf\n", (req_sec / CLIENTS));
}
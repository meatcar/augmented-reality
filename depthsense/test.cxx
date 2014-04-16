#include <stdlib.h>
#include <stdio.h>
#include <list>

// SAMPLE
using namespace std;
int main() {
    int matrix[20][30];
    for(int i = 0; i < 20; i++) {
        for(int j = 0; j < 30; j++) {
            matrix[i][j] = (i*j) % 4;
            if (i > 2 && i < 5 && j > 8 && j < 16) 
                matrix[i][j] = 2;

            if (i > 6 && i < 8 && j > 0 && j < 7) 
                matrix[i][j] = 1;

        }
    }

    printf("[ ");
    for(int i = 0; i < 20; i++) {
        for(int j = 0; j < 30; j++) {
            if (j == 0) {
                printf("[ %d, ", matrix[i][j]);
            } else if (j != 29) {
                printf("%d, ", matrix[i][j]);
            } else {
                printf("%d]", matrix[i][j]);
            }
            
        }

        if (i != 19) { 
            printf("\n");
        } else {
            printf(" ]\n");
        }
    }

    list<int *> queue;
    int visited[20][30];
    int result[20][30];
    for(int i = 0; i < 20; i++) {
        for(int j = 0; j < 30; j++) {
            visited[i][j] = 0;
            result[i][j] = 0;
        }
    }


    int *pack = (int *)malloc(sizeof(int) * 3);
    pack[0] = 4;
    pack[1] = 11;
    pack[2] = matrix[4][11];

    queue.push_back(pack);
    visited[4][11] = 1;
    result[4][11] = 2;

    while(!queue.empty()){
        int * val = queue.front();
        queue.pop_front();
        int p_i = val[0];
        int p_j = val[1];
        int v = val[2];
        printf("START: val : %d %d %d\n", p_i, p_j, v);
        // RIGHT
        if ((p_i + 1) < 20 && (visited[p_i + 1][p_j] == 0) && (matrix[p_i + 1][p_j] == v)) { 
            printf("val : %d %d %d PASS RIGHT\n", p_i + 1, p_j, v);
            int *pack = (int *)malloc(sizeof(int) * 3);
            pack[0] = p_i + 1;
            pack[1] = p_j;
            pack[2] = matrix[p_i + 1][p_j];
            queue.push_back(pack);
            result[p_i + 1][p_j] = v;
            visited[p_i + 1][p_j] = 1;
        }

        // LEFT
        if ((p_i - 1) > 0 && (visited[p_i - 1][p_j] == 0) && (matrix[p_i - 1][p_j] == v)) { 
            printf("val : %d %d %d PASS LEFT\n", p_i - 1, p_j, v);
            int *pack = (int *)malloc(sizeof(int) * 3);
            pack[0] = p_i - 1;
            pack[1] = p_j;
            pack[2] = matrix[p_i - 1][p_j];
            queue.push_back(pack);
            result[p_i - 1][p_j] = v;
            visited[p_i - 1][p_j] = 1;
        }

        // UP
        if ((p_j - 1) > 0 && (visited[p_i][p_j - 1] == 0) && (matrix[p_i][p_j - 1] == v)) { 
            printf("val : %d %d %d PASS UP\n", p_i, p_j - 1, v);
            int *pack = (int *)malloc(sizeof(int) * 3);
            pack[0] = p_i;
            pack[1] = p_j - 1;
            pack[2] = matrix[p_i][p_j - 1];
            queue.push_back(pack);

            result[p_i][p_j - 1] = v;
            visited[p_i][p_j - 1] = 1;
        }

        // DOWN
        if ((p_j + 1) < 30 && (visited[p_i][p_j + 1] == 0) && (matrix[p_i][p_j + 1] == v)) { 
            printf("val : %d %d %d PASS DOWN\n", p_i, p_j + 1, v);
            int *pack = (int *)malloc(sizeof(int) * 3);
            pack[0] = p_i;
            pack[1] = p_j + 1;
            pack[2] = matrix[p_i][p_j + 1];
            queue.push_back(pack);

            result[p_i][p_j + 1] = v;
            visited[p_i][p_j + 1] = 1;
        }

        free(val);
    }

    printf("----------\n");
    printf("[ ");
    for(int i = 0; i < 20; i++) {
        for(int j = 0; j < 30; j++) {
            if (j == 0) {
                printf("[ %d, ", result[i][j]);
            } else if (j != 29) {
                printf("%d, ", result[i][j]);
            } else {
                printf("%d]", result[i][j]);
            }
            
        }

        if (i != 19) { 
            printf("\n");
        } else {
            printf(" ]\n");
        }
    }

    printf("done\n");
    return 0;
}

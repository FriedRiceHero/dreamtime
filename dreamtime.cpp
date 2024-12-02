#include<iostream>
#include<array>
#include<memory>

template<std::size_t N>
struct vector {
    std::array<float,N> x;

    int nDim(){
        return N;
    }


    vector operator+(vector v){
        vector<N> res;

        for(int i=0;i<N;i++){
            res[i]=x[i]+v[i];
        }

        return res;
    }

    float& operator[](int n){
        return x[n];
    }

    friend std::ostream& operator<<(std::ostream& stream, const vector<N>& v){
        stream<<'['<<' ';
        for (const float f:v.x){
            stream<<f<<' ';
        }
        stream<<']';
        return stream;
    }
    

    
};


int main(){

    vector<3> x = {1,2,3};
    vector<3> y = {4.55,2/3,6*2};
    vector<3> r=y;
    std::cout<<r;
    float z=2/3;
    std::cout<<z;


};




#include<iostream>
#include<array>
#include<memory>
#include<cmath>

template<std::size_t N>
struct vector {
    std::array<double,N> x;
    
    int nDim(){
        return N;
    }

    double& operator[](int n){
        return x[n];
    }

    double magnitude(){
        double res=0;
        for(int i=0;i<N;i++){
            res=res+pow(x[i],2);
        }
        return sqrt(res);
    }

    vector direction(){
        vector<N> res=*this/this->magnitude();
        return res;
    }

    friend vector operator+(vector<N> u, vector<N> v){
        vector<N> res;
        for(int i=0;i<N;i++){
            res[i]=u[i]+v[i];
        }
        return res;
    }

    friend vector operator-(vector<N> u, vector<N> v){
        vector <N> res;
        for(int i=0;i<N;i++){
            res[i]=u[i]-v[i];
        }
        return res;
    }

    friend vector operator-(vector<N> v){
        vector <N> res;
        for(int i=0;i<N;i++){
            res[i]=-v[i];
        }
        return res;
    }

    friend vector operator*(vector<N> v,double y){
        vector<N> res;
        for(int i=0;i<N;i++){
            res[i]=y*v[i];
        }
        return res;
    }

    friend vector operator*(double y,vector<N> v){
        return v*y;
    }

    friend double operator*(vector<N> u,vector<N> v){
        double res=0;
        for(int i=0;i<N;i++){
            res=res+u[i]*v[i];
        }
        return res;
    }

    friend vector operator/(vector<N> v, double y){
        vector<N> res;
        for(int i=0;i<N;i++){
            res[i]=v[i]/y;
        }
        return res;
    }

    friend std::ostream& operator<<(std::ostream& stream, const vector<N>& v){
        stream<<'['<<' ';
        for (const double f:v.x){
            stream<<f<<' ';
        }
        stream<<']';
        return stream;
    }
};


int main(){

    vector<3> x = {1,2,3};
    vector<3> y = {4.55,2./3,6*2};
    vector<3> z = x.direction();
    std::cout<<z;


};




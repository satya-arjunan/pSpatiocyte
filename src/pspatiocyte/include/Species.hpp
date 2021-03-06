#ifndef __SPECIES_HPP
#define __SPECIES_HPP

#include <iostream>
#include <string>
#include <limits>
#include "Vector.hpp"
#include "Common.hpp"

class Species {
public:
  Species() {}
  Species(string n, double D, unsigned init_size, World& world, double P=1);
  Species(const Species &s);
  ~Species() {} 
  string get_name() {
    return name_;
  } 
  double getD() {
    return D_;
  }
  double get_walk_interval() {
    return walk_interval_*walk_probability_;
  } 
  int get_id() {
    return species_id_;
  } 
  void setVolumeDt(double rv) { 
    const double alpha = 2.0/3.0;
    walk_interval_ = (D_ > 0) ? alpha*rv*rv/D_ :
      std::numeric_limits<double>::infinity();
  } 
  void setSurfaceDt(double rv) {
    const double SQR2  = 1.414213562373;  
    const double SQR3  = 1.732050807569; 
    const double SQR6  = 2.449489742783;
    const double SQR22 = 4.690415759823;
    const double sqra = ( 2*SQR2 + 4*SQR3 + 3*SQR6 + SQR22 )/
                        ( 6*SQR2 + 4*SQR3 + 3*SQR6 );
    walk_interval_ = (D_ > 0) ? sqra*sqra*rv*rv/D_ :
      std::numeric_limits<double>::infinity(); 
  } 
  void set_rho(double rho) {
    rho_ = rho;
  } 
  void calcCollisionTime() { 
    if (rho_ > P_) {
      walk_probability_ = P_/rho_;
    }
  } 
  float get_walk_probability() {
    return walk_probability_;
  } 
  bool operator==(const Species &s) const {
    return name_==s.name_ && species_id_==s.species_id_;
  } 
  unsigned get_init_size() {
    return init_size_;
  }
  void set_populate_origin(const Vector<float>& origin) {
    populate_origin_ = origin;
  }
  void set_populate_range(const Vector<float>& range) {
    populate_range_ = range;
  }
  const Vector<float>& get_populate_origin() const {
    return populate_origin_;
  }
  const Vector<float>& get_populate_range() const {
    return populate_range_;
  }
private:
  string name_;        // name of species
  double D_ = 0;     // diffusion coefficient
  double P_ = 1; // user-defined upper limit of reaction probability
  unsigned init_size_ = 0;
  double walk_probability_ = 1;
  // diffusion step interval time
  double walk_interval_ = std::numeric_limits<double>::infinity();
  double rho_;         // max reaction probability [max(p_j)] of all reactions
  int species_id_;
  Vector<float> populate_origin_ = Vector<float>(0.5, 0.5, 0.5);
  Vector<float> populate_range_ = Vector<float>(1, 1, 1);
};

#endif /* __SPECIES_HPP */

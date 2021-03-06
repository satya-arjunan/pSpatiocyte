//::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
//
//        This file is part of pSpatiocyte
//
//        Copyright (C) 2019 Satya N.V. Arjunan
//
//::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
//
//
// Motocyte is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public
// License as published by the Free Software Foundation; either
// version 2 of the License, or (at your option) any later version.
// 
// Motocyte is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public
// License along with Motocyte -- see the file COPYING.
// If not, write to the Free Software Foundation, Inc.,
// 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
// 
//END_HEADER
//
// written by Satya Arjunan <satya.arjunan@gmail.com>
// and Atsushi Miyauchi
//



#include "Species.hpp"
#include "World.hpp"

Species::Species(string n, double D,  unsigned init_size,
                 World& world, double P):
  name_(n),
  D_(D),
  P_(std::min(P, 1.0)),
  init_size_(init_size),
  walk_interval_(std::numeric_limits<double>::infinity()),
  species_id_(world.add_species(this)) {}

Species::Species(const Species &s) {
  name_ = s.name_;
  D_ = s.D_;
  walk_interval_ = s.walk_interval_;
  P_ = s.P_;
  rho_ = s.rho_;
  walk_probability_ = s.walk_probability_;
  species_id_ = s.species_id_;
}



/******************************************************************************
*       SOFA, Simulation Open-Framework Architecture, development version     *
*                (c) 2006-2016 INRIA, USTL, UJF, CNRS, MGH                    *
*                                                                             *
* This library is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This library is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this library; if not, write to the Free Software Foundation,     *
* Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.          *
*******************************************************************************
*                               SOFA :: Plugins                               *
*                                                                             *
* Authors: The SOFA Team and external contributors (see Authors.txt)          *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/
#ifndef FRAME_FRAMEMECHANICALOBJECT_H
#define FRAME_FRAMEMECHANICALOBJECT_H

#include <SofaBaseMechanics/MechanicalObject.h>
#include "QuadraticTypes.h"
#include "AffineTypes.h"
#include "DeformationGradientTypes.h"
#include "initFrame.h"

namespace sofa
{

namespace component
{

namespace container
{

#if defined(SOFA_EXTERN_TEMPLATE) && !defined(FRAME_FRAMEMECHANICALOBJECT_CPP)
#ifndef SOFA_FLOAT
extern template class SOFA_FRAME_API MechanicalObject<defaulttype::Affine3dTypes>;
extern template class SOFA_FRAME_API MechanicalObject<defaulttype::Quadratic3dTypes>;
extern template class SOFA_FRAME_API MechanicalObjectInternalData<defaulttype::DeformationGradient332dTypes>;
extern template class SOFA_FRAME_API MechanicalObject<defaulttype::DeformationGradient332dTypes>;
#endif
#ifndef SOFA_DOUBLE
extern template class SOFA_FRAME_API MechanicalObject<defaulttype::Affine3fTypes>;
extern template class SOFA_FRAME_API MechanicalObject<defaulttype::Quadratic3fTypes>;
extern template class SOFA_FRAME_API MechanicalObjectInternalData<defaulttype::DeformationGradient332fTypes>;
extern template class SOFA_FRAME_API MechanicalObject<defaulttype::DeformationGradient332fTypes>;
#endif
#endif

} // namespace container

} // namespace component

} // namespace sofa

#endif

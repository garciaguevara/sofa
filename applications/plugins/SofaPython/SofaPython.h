/******************************************************************************
*       SOFA, Simulation Open-Framework Architecture, version 1.0 RC 1        *
*                (c) 2006-2011 MGH, INRIA, USTL, UJF, CNRS                    *
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
#ifndef INITSOFAPYTHON_H
#define INITSOFAPYTHON_H


#include <sofa/helper/system/config.h>
#include <sofa/core/Plugin.h>

#ifdef SOFA_BUILD_SOFAPYTHON
#define SOFA_SOFAPYTHON_API SOFA_EXPORT_DYNAMIC_LIBRARY
#else
#define SOFA_SOFAPYTHON_API SOFA_IMPORT_DYNAMIC_LIBRARY
#endif

#define SOFAPYTHON_VERSION "0.2"

class PythonPlugin : public sofa::core::Plugin
{
public:
    PythonPlugin();
    SOFA_PLUGIN(PythonPlugin)

    virtual bool init();

    virtual bool exit() { return true; }
    virtual bool canBeUnloaded() { return false; }  // the scene loader annot be uninitialized yet

};

/** \mainpage
  This is a the starting page of the Python plugin documentation.
  */

#endif // INITEmptyPlugin_H
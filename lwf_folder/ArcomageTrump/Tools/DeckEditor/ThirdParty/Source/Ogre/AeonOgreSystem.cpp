/*
* Part of the Aeon Framework
* -----------------------------------------------------------------------------
* Aeon Ogre3D Integration Wrapper
*
* File:		OgreSystem.cpp
  Desc.:	Abstract Ogre System Base class.
* Author:	Felix Bruckner <xography@gatewayheaven.com>
*
* Copyright (c) 2009-2011, gatewayheaven.com. 
*
* Licensed under the Boost Software License.
*
* -----------------------------------------------------------------------------
* Permission is hereby granted, free of charge, to any person or organization
* obtaining a copy of the software and accompanying documentation covered by
* this license (the "Software") to use, reproduce, display, distribute,
* execute, and transmit the Software, and to prepare derivative works of the
* Software, and to permit third-parties to whom the Software is furnished to
* do so, all subject to the following:
* 
* The copyright notices in the Software and this entire statement, including
* the above license grant, this restriction and the following disclaimer,
* must be included in all copies of the Software, in whole or in part, and
* all derivative works of the Software, unless such copies or derivative
* works are solely in the form of machine-executable object code generated by
* a source language processor.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
* SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
* FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
* ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.
* -----------------------------------------------------------------------------
*/
#include <Ogre/AeonOgreSystem.h>

#include <OgrePrerequisites.h>
#include <OgreString.h>
#include <OgreRoot.h>
#include <OgreRenderWindow.h>
#include <OgreConfigFile.h>
#include <OgreWindowEventUtilities.h>
#include <OgreFrameListener.h>
#include <OgreLogManager.h>
#include <OgreLog.h>

#include <boost/foreach.hpp>

namespace Aeon {
	// ------------------------------------------------------------------------
	AeonOgreSystem::AeonOgreSystem() : windowTitle(""), isDebug(false), initialized(false) {

	}

	// ------------------------------------------------------------------------
	AeonOgreSystem::~AeonOgreSystem(void) {
		root->saveConfig();

		Ogre::WindowEventUtilities::removeWindowEventListener(renderWindow, this);
		renderWindow = 0;
	}

	// ------------------------------------------------------------------------
	void AeonOgreSystem::initialize( const Ogre::String& pluginConf,
		const Ogre::String& gameConf,
		const Ogre::String& gameLog
		) {
			Ogre::RenderSystem* sys = 0;
			Ogre::LogManager* _log = new Ogre::LogManager();

			try  {	
				log = Ogre::LogManager::getSingleton().createLog(gameLog, true, true, false);

				if(OGRE_DEBUG_MODE) {
					log->setDebugOutputEnabled(true);
				} else {
					log->setDebugOutputEnabled(false);
				}
			
				root = new Ogre::Root(pluginConf, gameConf);
			} catch(Ogre::Exception &e) {
				std::cout << e.what();
			}	

			//loadRendersystems("Plugins/");

			if(!root->restoreConfig()) {
				sys = selectRenderSystem();

				if(sys != 0)
					root->setRenderSystem(sys);
			} else {
				sys = root->getRenderSystem();
			}

			if(sys != 0) {
				root->initialise(false);

				// We're not creating windows here, this is subject to the
				// user, but sicne the sub system is initialized, we can use
				// the Renderer.
				initialized = true;
			}
			// root->setFrameSmoothingPeriod(1.0);
	}



	// ------------------------------------------------------------------------
	void AeonOgreSystem::loadRendersystems(const Ogre::String& path) {
		std::vector<Ogre::String> plugins;

		// Always offer the GL Rendersystem
		plugins.push_back(path + "RenderSystem_GL");

		// Only load the Direct X Rendersystems under Windows
		#if OGRE_PLATFORM == OGRE_PLATFORM_WIN32
			plugins.push_back(path + "RenderSystem_Direct3D9");

		// Unused, since still experimental:
			//plugins.push_back(path + "RenderSystem_Direct3D10");
			//plugins.push_back(path + "RenderSystem_Direct3D11");
		#endif


		BOOST_FOREACH( Ogre::String &p, plugins ) {
			#if defined(OGRE_DEBUG_MODE)
				p.append("_d");
			#endif

			root->loadPlugin(p + ((OGRE_PLATFORM == OGRE_PLATFORM_WIN32) ? ".dll" : ".so"));
		}
	}

	// ------------------------------------------------------------------------
	bool AeonOgreSystem::frameStarted(const Ogre::FrameEvent& evt) {
		return true;

	}
	// ------------------------------------------------------------------------
	bool AeonOgreSystem::frameRenderingQueued(const Ogre::FrameEvent& evt) {
		return true;

	}

	// ------------------------------------------------------------------------
	void AeonOgreSystem::windowResized(Ogre::RenderWindow* rw) {

	}

	// ------------------------------------------------------------------------
	void AeonOgreSystem::windowClosed(Ogre::RenderWindow* rw) {

	}
	// ------------------------------------------------------------------------
	void AeonOgreSystem::loadResources(const Ogre::String &prefix, 
									const Ogre::String &filename) {
		Ogre::ConfigFile cf;
		cf.load(filename);

		Ogre::ConfigFile::SectionIterator seci = cf.getSectionIterator();

		Ogre::String secName;

		while (seci.hasMoreElements()) {
			secName = seci.peekNextKey();
			Ogre::ConfigFile::SettingsMultiMap *settings = seci.getNext();

			for (Ogre::ConfigFile::SettingsMultiMap::iterator i
				= settings->begin(); i != settings->end(); ++i) {
					Ogre::ResourceGroupManager::getSingleton().addResourceLocation(
						prefix+i->second,i->first, secName);
			}
		}

	}


}
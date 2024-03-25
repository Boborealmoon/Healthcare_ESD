if( typeof jQuery !== 'undefined' ) {
	var $ = jQuery.noConflict();
}

(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
	typeof define === 'function' && define.amd ? define(factory) :
	( global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.SEMICOLON = factory() );
} (this, (function() {

	// USE STRICT
	"use strict";

	var options = {
		pageTransition: false,
		cursor: false,
		tips: false,
		headerSticky: true,
		headerMobileSticky: false,
		menuBreakpoint: 992,
		pageMenuBreakpoint: 992,
		gmapAPI: '',
		scrollOffset: 60,
		scrollExternalLinks: true,
		smoothScroll: false,	
		jsFolder: 'js/',
		cssFolder: 'css/',
	};

	if( typeof cnvsOptions !== 'undefined' ) {
		options = Object.assign({}, options, cnvsOptions);
	}

	var vars = {
		baseEl: document,
		elRoot: document.documentElement,
		elHead: document.head,
		elBody: document.body,
		viewport: {
			width: 0,
			height: 0,
		},
		hash: window.location.hash,
		topScrollOffset: 0,
		elWrapper: document.getElementById('wrapper'),
		elHeader: document.getElementById('header'),
		headerClasses: '',
		elHeaderWrap: document.getElementById('header-wrap'),
		headerWrapClasses: '',
		headerHeight: 0,
		headerOffset: 0,
		headerWrapHeight: 0,
		headerWrapOffset: 0,
		elPrimaryMenus: document.querySelectorAll('.primary-menu'),
		elPrimaryMenuTriggers: document.querySelectorAll('.primary-menu-trigger'),
		elPageMenu: document.getElementById('page-menu'),
		pageMenuOffset: 0,
		elSlider: document.getElementById('slider'),
		elFooter: document.getElementById('footer'),
		elAppMenu: document.querySelector('.app-menu'),
		portfolioAjax: {},
		sliderParallax: {
			el: document.querySelector('.slider-parallax'),
			caption: document.querySelector('.slider-parallax .slider-caption'),
			inner: document.querySelector('.slider-inner'),
			offset: 0,
		},
		get menuBreakpoint() {
			return this.elBody.getAttribute('data-menu-breakpoint') || options.menuBreakpoint;
		},
		get pageMenuBreakpoint() {
			return this.elBody.getAttribute('data-pagemenu-breakpoint') || options.pageMenuBreakpoint;
		},
		get customCursor() {
			var value = this.elBody.getAttribute('data-custom-cursor') || options.cursor;
			return value == 'true' || value === true ? true : false;
		},
		get pageTransition() {
			var value = this.elBody.classList.contains('page-transition') || options.pageTransition;
			return value == 'true' || value === true ? true : false;
		},
		get tips() {
			var value = this.elBody.getAttribute('data-tips') || options.tips;
			return value == 'true' || value === true ? true : false;
		},
		get smoothScroll() {
			var value = this.elBody.getAttribute('data-smooth-scroll') || options.smoothScroll;
			return value == 'true' || value === true ? true : false;
		},
		get isRTL() {
			return this.elRoot.getAttribute('dir') == 'rtl' ? true : false;
		},
		scrollPos: {
			x: 0,
			y: 0,
		},
		$jq: typeof jQuery !== "undefined" ? jQuery.noConflict() : '',
		resizers: {},
		recalls: {},
		debounced: false,
		events: {},
		modules: {},
		fn: {},
		required: {
			jQuery: {
				plugin: 'jquery',
				fn: function(){
					return typeof jQuery !== 'undefined';
				},
				file: options.jsFolder+'jquery.js',
				id: 'canvas-jquery',
			}
		},
		fnInit: function() {
			DocumentOnReady.init();
			DocumentOnLoad.init();
			DocumentOnResize.init();
		}
	};

	var Core = function() {
		return {
			getOptions: options,
			getVars: vars,

			run: function(obj) {
				Object.values(obj).map( function(fn) {
					return typeof fn === 'function' && fn.call();
				});
			},

			runBase: function() {
				Core.run(Base);
			},

			runModules: function() {
				Core.run(Modules);
			},

			runContainerModules: function(parent) {
				if( typeof parent === 'undefined' ) {
					return false;
				}

				Core.getVars.baseEl = parent;
				Core.runModules();
				Core.getVars.baseEl = document;
			},

			breakpoints: function() {
				var viewWidth = Core.viewport().width;

				var breakpoint = {
					xxl: {
						enter: 1400,
						exit: 99999
					},
					xl: {
						enter: 1200,
						exit: 1399
					},
					lg: {
						enter: 992,
						exit: 1199.98
					},
					md: {
						enter: 768,
						exit: 991.98
					},
					sm: {
						enter: 576,
						exit: 767.98
					},
					xs: {
						enter: 0,
						exit: 575.98
					}
				};

				var previous = '';

				Object.keys( breakpoint ).forEach( function(key) {
					if ( (viewWidth > breakpoint[key].enter) && (viewWidth <= breakpoint[key].exit) ) {
						vars.elBody.classList.add( 'device-'+key );
					} else {
						vars.elBody.classList.remove( 'device-'+key );
						if( previous != '' ) {
							vars.elBody.classList.remove( 'device-down-'+previous );
						}
					}

					if ( viewWidth <= breakpoint[key].exit ) {
						if( previous != '' ) {
							vars.elBody.classList.add( 'device-down-'+previous );
						}
					}

					previous = key;

					if ( viewWidth > breakpoint[key].enter ) {
						vars.elBody.classList.add( 'device-up-'+key );
						return;
					} else {
						vars.elBody.classList.remove( 'device-up-'+key );
					}
				});
			},

			colorScheme: function() {
				if( vars.elBody.classList.contains('adaptive-color-scheme') ) {
					window.matchMedia('(prefers-color-scheme: dark)').matches ? vars.elBody.classList.add( 'dark' ) : vars.elBody.classList.remove('dark');
				}

				var bodyColorScheme = Core.cookie.get('__cnvs_body_color_scheme');

				if( bodyColorScheme && bodyColorScheme != '' ) {
					bodyColorScheme.split(" ").includes('dark') ? vars.elBody.classList.add( 'dark' ) : vars.elBody.classList.remove( 'dark' );
				}
			},

			throttle: function(timer, func, delay) {
				if(timer) {
					return;
				}

				timer = setTimeout( function() {
					func();
					timer = undefined;
				}, delay);
			},

			debounce: function(callback, delay) {
				clearTimeout(vars.debounced);
				vars.debounced = setTimeout(callback, delay);
			},

			debouncedResize: function(func, delay) {
				var timeoutId;
				return function() {
					var context = this;
					var args = arguments;
					clearTimeout(timeoutId);
					timeoutId = setTimeout( function() {
						func.apply(context, args);
					}, delay);
				};
			},

			addEvent: function(el, event, args = {}) {
				if( typeof el === "undefined" || typeof event === "undefined" ) {
					return;
				}

				var createEvent = new CustomEvent( event, {
					detail: args
				});

				el.dispatchEvent( createEvent );
				vars.events[event] = true;
			},

			scrollEnd: function(callback, refresh = 199) {
				if (!callback || typeof callback !== 'function') return;

				window.addEventListener('scroll', function() {
					Core.debounce( callback, refresh );
				}, {passive: true});
			},

			viewport: function() {
				var viewport = {
					width: window.innerWidth || vars.elRoot.clientWidth,
					height: window.innerHeight || vars.elRoot.clientHeight
				};

				vars.viewport = viewport;

				document.documentElement.style.setProperty('--GD-viewport-width', viewport.width);
				document.documentElement.style.setProperty('--GD-viewport-height', viewport.height);
				document.documentElement.style.setProperty('--GD-body-height', vars.elBody.clientHeight);

				return viewport;
			},

			isElement: function(selector) {
				if (typeof selector === 'object' && selector !== null) {
					return true;
				}

				if (selector instanceof Element || selector instanceof HTMLElement) {
					return true;
				}

				if (typeof selector.jquery !== 'undefined') {
					selector = selector[0];
				}

				if (typeof selector.nodeType !== 'undefined') {
					return true;
				}

				return false;
			},

			getSelector: function(selector, jquery=true, customjs=true) {
				if(jquery) {
					if( Core.getVars.baseEl !== document ) {
						selector = jQuery(Core.getVars.baseEl).find(selector);
					} else {
						selector = jQuery(selector);
					}

					if( customjs ) {
						if( typeof customjs == 'string' ) {
							selector = selector.filter(':not('+ customjs +')');
						} else {
							selector = selector.filter(':not(.customjs)');
						}
					}
				} else {
					if( Core.isElement(selector) ) {
						selector = selector;
					} else {
						if( customjs ) {
							if( typeof customjs == 'string' ) {
								selector = Core.getVars.baseEl.querySelectorAll(selector+':not('+customjs+')');
							} else {
								selector = Core.getVars.baseEl.querySelectorAll(selector+':not(.customjs)');
							}
						} else {
							selector = Core.getVars.baseEl.querySelectorAll(selector);
						}
					}
				}

				return selector;
			},

			onResize: function(callback, refresh = 333) {
				if (!callback || typeof callback !== 'function') return;

				window.addEventListener('resize', function() {
					Core.debounce( callback, refresh );
				});
			},

			imagesLoaded: function(el) {
				var imgs = el.getElementsByTagName('img') || document.images,
					len = imgs.length,
					counter = 0;

				if(len < 1) {
					Core.addEvent(el, 'CanvasImagesLoaded');
				}

				var incrementCounter = async function() {
					counter++;
					if(counter === len) {
						Core.addEvent(el, 'CanvasImagesLoaded');
					}
				};

				[].forEach.call( imgs, function( img ) {
					if(img.complete) {
						incrementCounter();
					} else {
						img.addEventListener('load', incrementCounter, false);
					}
				});
			},

			contains: function(classes, selector) {
				var classArray = classes.split(" ");
				var hasClass = false;

				classArray.forEach( function(classTxt) {
					if( vars.elBody.classList.contains(classTxt) ) {
						hasClass = true;
					}
				});

				return hasClass;
			},

			has: function(nodeList, selector) {
				return [].slice.call(nodeList)?.filter( function(e) {
					return e.querySelector(selector);
				});
			},

			filtered: function(nodeList, selector) {
				return [].slice.call(nodeList)?.filter( function(e) {
					return e.matches(selector);
				});
			},

			parents: function(elem, selector) {
				if (!Element.prototype.matches) {
					Element.prototype.matches =
						Element.prototype.matchesSelector ||
						Element.prototype.mozMatchesSelector ||
						Element.prototype.msMatchesSelector ||
						Element.prototype.oMatchesSelector ||
						Element.prototype.webkitMatchesSelector ||
						function(s) {
							var matches = (this.document || this.ownerDocument).querySelectorAll(s),
								i = matches.length;
							while (--i >= 0 && matches.item(i) !== this) {}
							return i > -1;
						};
				}

				var parents = [];

				for ( ; elem && elem !== document; elem = elem.parentNode ) {
					if (selector) {
						if (elem.matches(selector)) {
							parents.push(elem);
						}
						continue;
					}
					parents.push(elem);
				}

				return parents;
			},

			siblings: function(elem, nodes = false) {
				if( nodes ) {
					return [].slice.call(nodes).filter( function(sibling) {
						return sibling !== elem;
					});
				} else {
					return [].slice.call(elem.parentNode.children).filter( function(sibling) {
						return sibling !== elem;
					});
				}
			},

			getNext: function(elem, selector) {
				var nextElem = elem.nextElementSibling;

				if( !selector ) {
					return nextElem;
				}

				if( nextElem && nextElem.matches(selector) ) {
					return nextElem;
				}

				return null;
			},

			offset: function(el) {
				var rect = el.getBoundingClientRect(),
					scrollLeft = window.scrollX || document.documentElement.scrollLeft,
					scrollTop = window.scrollY || document.documentElement.scrollTop;

				return {top: rect.top + scrollTop, left: rect.left + scrollLeft};
			},

			isHidden: function(el) {
				return (el.offsetParent === null);
			},

			classesFn: function(func, classes, selector) {
				var classArray = classes.split(" ");
				classArray.forEach( function(classTxt) {
					if( func == 'add' ) {
						selector.classList.add(classTxt);
					} else if( func == 'toggle' ) {
						selector.classList.toggle(classTxt);
					} else {
						selector.classList.remove(classTxt);
					}
				});
			},

			cookie: function() {
				return {
					set: function(name, value, daysToExpire) {
						var date = new Date();
						date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
						var expires = "expires=" + date.toUTCString();
						document.cookie = name + "=" + value + ";" + expires + ";path=/";
					},

					get: function(name) {
						var decodedCookies = decodeURIComponent(document.cookie);
						var cookies = decodedCookies.split(";");

						for (let i = 0; i < cookies.length; i++) {
						  var cookie = cookies[i].trim();
						  if (cookie.startsWith(name + "=")) {
							return cookie.substring(name.length + 1);
						  }
						}

						return null;
					},

					remove: function(name) {
						document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
					}
				};
			}(),

			scrollTo: function(offset = 0, speed = 1250, easing, behavior = 'smooth') {
				if( easing && (typeof jQuery !== 'undefined' && typeof jQuery.easing["easeOutQuad"] !== 'undefined') ) {
					jQuery('body,html').stop(true).animate({
						'scrollTop': Number(offset)
					}, Number( speed ), easing );
				} else {
					var smoothScroll = 'scrollBehavior' in document.documentElement.style;

					if( typeof window.scroll === 'function' && smoothScroll ) {
						window.scroll({
							top: Number(offset),
							behavior: behavior
						});
					} else {
						var body = Core.getVars.elBody;
						var rootEl = Core.getVars.elRoot;

						body.scrollIntoView();
						rootEl.scrollIntoView();

						var scrollToTop = function() {
							if (body.scrollTop > Number(offset) || rootEl.scrollTop > Number(offset)) {
								body.scrollTop -= 20;
								rootEl.scrollTop -= 20;
								setTimeout(scrollToTop, 10);
							}
						};

						scrollToTop();
					}
				}
			},

			smoothScroll: function() {
				new initSmoothScrollfunction(document,90,5);

				function initSmoothScrollfunction(target, speed, smooth) {
					if (target === document)
						target = (document.scrollingElement
							  || document.documentElement
							  || document.body.parentNode
							  || document.body); // cross browser support for document scrolling

					var moving = false;
					var pos = target.scrollTop;
					 var frame = target === document.body
							  && document.documentElement
							  ? document.documentElement
							  : target; // safari is the new IE

					target.addEventListener('mousewheel', scrolled, { passive: false });
					target.addEventListener('DOMMouseScroll', scrolled, { passive: false });

					function scrolled(e) {
						e.preventDefault(); // disable default scrolling

						var delta = normalizeWheelDelta(e);

						pos += -delta * speed;
						pos = Math.max(0, Math.min(pos, target.scrollHeight - frame.clientHeight)); // limit scrolling

						if (!moving) update();
					}

					function normalizeWheelDelta(e){
						if(e.detail){
							if(e.wheelDelta)
								return e.wheelDelta/e.detail/40 * (e.detail>0 ? 1 : -1); // Opera
							else
								return -e.detail/3; // Firefox
						}else
							return e.wheelDelta/120; // IE,Safari,Chrome
					};

					function update() {
						moving = true;

						var delta = (pos - target.scrollTop) / smooth;

						target.scrollTop += delta;

						if (Math.abs(delta) > 0.5)
							requestFrame(update);
						else
							moving = false;
					}

					var requestFrame = function() { // requestAnimationFrame cross browser
						return (
							window.requestAnimationFrame ||
							window.webkitRequestAnimationFrame ||
							window.mozRequestAnimationFrame ||
							window.oRequestAnimationFrame ||
							window.msRequestAnimationFrame ||
							function(func) {
								window.setTimeout(func, 1000 / 50);
							}
						);
					}();
				}
			},

			loadCSS: function(params) {
				var file = params.file;
				var htmlID = params.id || false;
				var cssFolder = params.cssFolder || false;

				if( !file ) {
					return false;
				}

				if( htmlID && document.getElementById(htmlID) ) {
					return false;
				}

				var htmlStyle = document.createElement('link');

				htmlStyle.id = htmlID;
				htmlStyle.href = cssFolder ? options.cssFolder+file : file;
				htmlStyle.rel = 'stylesheet';
				htmlStyle.type = 'text/css';

				vars.elHead.appendChild(htmlStyle);
				return true;
			},

			loadJS: function(params) {
				var file = params.file;
				var htmlID = params.id || false;
				var type = params.type || false;
				var callback = params.callback;
				var async = params.async || true;
				var defer = params.defer || true;
				var jsFolder = params.jsFolder || false;

				if( !file ) {
					return false;
				}

				if( htmlID && document.getElementById(htmlID) ) {
					return false;
				}

				var htmlScript = document.createElement('script');

				if ( typeof callback !== 'undefined' ) {
					if( typeof callback != 'function' ) {
						throw new Error('Not a valid callback!');
					} else {
						htmlScript.onload = callback;
					}
				}

				htmlScript.id = htmlID;
				htmlScript.src = jsFolder ? options.jsFolder+file : file;
				if( type ) {
					htmlScript.type = type;
				}
				htmlScript.async = async ? true : false;
				htmlScript.defer = defer ? true : false;

				vars.elBody.appendChild(htmlScript);
				return true;
			},

			isFuncTrue: async function(fn) {
				if( 'function' !== typeof fn ) {
					return false;
				}

				var counter = 0;

				return new Promise( function(resolve, reject) {
					if(fn()) {
						resolve(true);
					} else {
						var int = setInterval( function() {
							if(fn()) {
								clearInterval( int );
								resolve(true);
							} else {
								if( counter > 30 ) {
									clearInterval( int );
									reject(true);
								}
							}
							counter++;
						}, 333);
					}
				}).catch( function(error) {
					console.log('Function does not exist: ' + fn);
				});
			},

			initFunction: function(params) {
				vars.elBody.classList.add(params.class);
				Core.addEvent(window, params.event);
				vars.events[params.event] = true;
			},

			topScrollOffset: function() {
				var topOffsetScroll = 0;
				var pageMenuOffset = vars.elPageMenu?.querySelector('#page-menu-wrap')?.offsetHeight || 0;

				if( vars.elBody.classList.contains('is-expanded-menu') ) {
					if( vars.elHeader?.classList.contains('sticky-header') ) {
						topOffsetScroll = vars.elHeaderWrap.offsetHeight;
					}

					if( vars.elPageMenu?.classList.contains('dots-menu') ) {
						pageMenuOffset = 0;
					}
				}

				topOffsetScroll = topOffsetScroll + pageMenuOffset;

				Core.getVars.topScrollOffset = topOffsetScroll + options.scrollOffset;
			},
		};
	}();

	var Base = function() {
		return {
			init: function() {
				Mobile.any() && vars.elBody.classList.add('device-touch');
			},

			menuBreakpoint: function() {
				if( Core.getVars.menuBreakpoint <= Core.viewport().width ) {
					vars.elBody.classList.add( 'is-expanded-menu' );
				} else {
					vars.elBody.classList.remove( 'is-expanded-menu' );
				}

				if( vars.elPageMenu ) {
					if( typeof Core.getVars.pageMenuBreakpoint === 'undefined' ) {
						Core.getVars.pageMenuBreakpoint = Core.getVars.menuBreakpoint;
					}

					if( Core.getVars.pageMenuBreakpoint <= Core.viewport().width ) {
						vars.elBody.classList.add( 'is-expanded-pagemenu' );
					} else {
						vars.elBody.classList.remove( 'is-expanded-pagemenu' );
					}
				}
			},

			stickFooterOnSmall: function() {
				CNVS.StickFooterOnSmall && CNVS.StickFooterOnSmall.init('#footer');
			},

			pageMenu: function() {
				CNVS.PageMenu && CNVS.PageMenu.init('#page-menu');
			},

			sliderDimensions: function() {
				CNVS.SliderDimensions && CNVS.SliderDimensions.init('.slider-element');
			},

			sliderMenuClass: function() {
				CNVS.SliderMenuClass && CNVS.SliderMenuClass.init('.transparent-header + .swiper_wrapper,.swiper_wrapper + .transparent-header,.transparent-header + .revslider-wrap,.revslider-wrap + .transparent-header');
			},

			sidePanel: function() {
				CNVS.SidePanel && CNVS.SidePanel.init('#side-panel');
			},

			adaptiveColorScheme: function() {
				CNVS.AdaptiveColorScheme && CNVS.AdaptiveColorScheme.init('.adaptive-color-scheme');
			},

			portfolioAjax: function() {
				CNVS.PortfolioAjax && CNVS.PortfolioAjax.init('.portfolio-ajax');
			},

			cursor: function() {
				if( vars.customCursor ) {
					CNVS.Cursor && CNVS.Cursor.init('body');
				}
			},

			setBSTheme: function() {
				if( vars.elBody.classList.contains('dark') ) {
					document.querySelector('html').setAttribute('data-bs-theme', 'dark');
				} else {
					document.querySelector('html').removeAttribute('data-bs-theme');
					document.querySelectorAll('.dark')?.forEach( function(el) {
						el.setAttribute('data-bs-theme', 'dark');
					});
				}

				vars.elBody.querySelectorAll('.not-dark')?.forEach( function(el) {
					el.setAttribute('data-bs-theme', 'light');
				});
			}
		}
	}();

	var Modules = function() {
		return {
			bootstrap: function() {
				var notExec = true;
				document.querySelectorAll('*').forEach( function(el) {
					if( notExec ) {
						el.getAttributeNames().some( function(text) {
							if( text.includes('data-bs') ) {
								notExec = false;
								CNVS.Bootstrap && CNVS.Bootstrap.init('body');
								return true;
							}
						});
					}
				});
			},

			resizeVideos: function(element) {
				CNVS.ResizeVideos && CNVS.ResizeVideos.init(element ? element : 'iframe[src*="youtube"],iframe[src*="vimeo"],iframe[src*="dailymotion"],iframe[src*="maps.google.com"],iframe[src*="google.com/maps"]');
			},

			pageTransition: function() {
				if( vars.pageTransition ) {
					CNVS.PageTransition && CNVS.PageTransition.init('body');
				}
			},

			lazyLoad: function(element) {
				CNVS.LazyLoad && CNVS.LazyLoad.init(element ? element : '.lazy:not(.lazy-loaded)');
			},

			dataClasses: function() {
				CNVS.DataClasses && CNVS.DataClasses.init('[data-class]');
			},

			dataHeights: function() {
				CNVS.DataHeights && CNVS.DataHeights.init('[data-height-xxl],[data-height-xl],[data-height-lg],[data-height-md],[data-height-sm],[data-height-xs]');
			},

			lightbox: function(element) {
				CNVS.Lightbox && CNVS.Lightbox.init(element ? element : '[data-lightbox]');
			},

			modal: function(element) {
				CNVS.Modal && CNVS.Modal.init(element ? element : '.modal-on-load');
			},

			animations: function(element) {
				CNVS.Animations && CNVS.Animations.init(element ? element : '[data-animate]');
			},

			hoverAnimations: function(element) {
				CNVS.HoverAnimations && CNVS.HoverAnimations.init(element ? element : '[data-hover-animate]');
			},

			gridInit: function(element) {
				CNVS.Grid && CNVS.Grid.init(element ? element : '.grid-container');
			},

			filterInit: function(element) {
				CNVS.Filter && CNVS.Filter.init(element ? element : '.grid-filter,.custom-filter');
			},

			canvasSlider: function(element) {
				CNVS.CanvasSlider && CNVS.CanvasSlider.init(element ? element : '.swiper_wrapper');
			},

			sliderParallax: function() {
				CNVS.SliderParallax && CNVS.SliderParallax.init('.slider-parallax');
			},

			flexSlider: function(element) {
				CNVS.FlexSlider && CNVS.FlexSlider.init(element ? element : '.fslider');
			},

			html5Video: function(element) {
				CNVS.FullVideo && CNVS.FullVideo.init(element ? element : '.video-wrap');
			},

			youtubeBgVideo: function(element) {
				CNVS.YoutubeBG && CNVS.YoutubeBG.init(element ? element : '.yt-bg-player');
			},

			toggle: function(element) {
				CNVS.Toggle && CNVS.Toggle.init(element ? element : '.toggle');
			},

			accordion: function(element) {
				CNVS.Accordion && CNVS.Accordion.init(element ? element : '.accordion');
			},

			counter: function(element) {
				CNVS.Counter && CNVS.Counter.init(element ? element : '.counter');
			},

			countdown: function(element) {
				CNVS.Countdown && CNVS.Countdown.init(element ? element : '.countdown');
			},

			gmap: function(element) {
				CNVS.GoogleMaps && CNVS.GoogleMaps.init(element ? element : '.gmap');
			},

			roundedSkills: function(element) {
				CNVS.RoundedSkills && CNVS.RoundedSkills.init(element ? element : '.rounded-skill');
			},

			progress: function(element) {
				CNVS.Progress && CNVS.Progress.init(element ? element : '.skill-progress');
			},

			twitterFeed: function(element) {
				CNVS.Twitter && CNVS.Twitter.init(element ? element : '.twitter-feed');
			},

			flickrFeed: function(element) {
				CNVS.Flickr && CNVS.Flickr.init(element ? element : '.flickr-feed');
			},

			instagram: function(element) {
				CNVS.Instagram && CNVS.Instagram.init(element ? element : '.instagram-photos');
			},

			// Dribbble Pending

			navTree: function(element) {
				CNVS.NavTree && CNVS.NavTree.init(element ? element : '.nav-tree');
			},

			carousel: function(element) {
				CNVS.Carousel && CNVS.Carousel.init(element ? element : '.carousel-widget');
			},

			masonryThumbs: function(element) {
				CNVS.MasonryThumbs && CNVS.MasonryThumbs.init(element ? element : '.masonry-thumbs');
			},

			notifications: function(element) {
				CNVS.Notifications && CNVS.Notifications.init(element ? element : false);
			},

			textRotator: function(element) {
				CNVS.TextRotator && CNVS.TextRotator.init(element ? element : '.text-rotater');
			},

			onePage: function(element) {
				CNVS.OnePage && CNVS.OnePage.init(element ? element : '[data-scrollto],.one-page-menu');
			},

			ajaxForm: function(element) {
				CNVS.AjaxForm && CNVS.AjaxForm.init(element ? element : '.form-widget');
			},

			subscribe: function(element) {
				CNVS.Subscribe && CNVS.Subscribe.init(element ? element : '.subscribe-widget');
			},

			conditional: function(element) {
				CNVS.Conditional && CNVS.Conditional.init(element ? element : '.form-group[data-condition],.form-group[data-conditions]');
			},

			shapeDivider: function(element) {
				CNVS.ShapeDivider && CNVS.ShapeDivider.init(element ? element : '.shape-divider');
			},

			stickySidebar: function(element) {
				CNVS.StickySidebar && CNVS.StickySidebar.init(element ? element : '.sticky-sidebar-wrap');
			},

			cookies: function(element) {
				CNVS.Cookies && CNVS.Cookies.init(element ? element : '.gdpr-settings,[data-cookies]');
			},

			quantity: function(element) {
				CNVS.Quantity && CNVS.Quantity.init(element ? element : '.quantity');
			},

			readmore: function(element) {
				CNVS.ReadMore && CNVS.ReadMore.init(element ? element : '[data-readmore]');
			},

			pricingSwitcher: function(element) {
				CNVS.PricingSwitcher && CNVS.PricingSwitcher.init(element ? element : '.pricing-tenure-switcher');
			},

			ajaxButton: function(element) {
				CNVS.AjaxButton && CNVS.AjaxButton.init(element ? element : '[data-ajax-loader]');
			},

			videoFacade: function(element) {
				CNVS.VideoFacade && CNVS.VideoFacade.init(element ? element : '.video-facade');
			},

			schemeToggle: function(element) {
				CNVS.SchemeToggle && CNVS.SchemeToggle.init(element ? element : '.body-scheme-toggle');
			},

			clipboardCopy: function(element) {
				CNVS.Clipboard && CNVS.Clipboard.init(element ? element : '.clipboard-copy');
			},

			codeHighlight: function(element) {
				CNVS.CodeHighlight && CNVS.CodeHighlight.init(element ? element : '.code-highlight');
			},

			tips: function() {
				if( vars.tips ) {
					CNVS.Tips && CNVS.Tips.init('body');
				}
			},

			textSplitter: function(element) {
				CNVS.TextSplitter && CNVS.TextSplitter.init(element ? element : '.text-splitter');
			},

			mediaActions: function(element) {
				CNVS.MediaActions && CNVS.MediaActions.init(element ? element : '.media-wrap');
			},

			viewportDetect: function(element) {
				CNVS.ViewportDetect && CNVS.ViewportDetect.init(element ? element : '.viewport-detect');
			},

			scrollDetect: function(element) {
				CNVS.ScrollDetect && CNVS.ScrollDetect.init(element ? element : '.scroll-detect');
			},

			fontSizer: function(element) {
				CNVS.FontSizer && CNVS.FontSizer.init(element ? element : '.font-sizer');
			},

			hover3D: function(element) {
				CNVS.Hover3D && CNVS.Hover3D.init(element ? element : '.hover-3d');
			},

			bsComponents: function(element) {
				CNVS.BSComponents && CNVS.BSComponents.init(element ? element : '[data-bs-toggle="tooltip"],[data-bs-toggle="popover"],[data-bs-toggle="tab"],[data-bs-toggle="pill"],.style-msg');
			}
		};
	}();

	var Mobile = function() {
		return {
			Android: function()  {
				return navigator.userAgent.match(/Android/i);
			},
			BlackBerry: function()  {
				return navigator.userAgent.match(/BlackBerry/i);
			},
			iOS: function()  {
				return navigator.userAgent.match(/iPhone|iPad|iPod/i);
			},
			Opera: function()  {
				return navigator.userAgent.match(/Opera Mini/i);
			},
			Windows: function()  {
				return navigator.userAgent.match(/IEMobile/i);
			},
			any: function()  {
				return (Mobile.Android() || Mobile.BlackBerry() || Mobile.iOS() || Mobile.Opera() || Mobile.Windows());
			}
		}
	}();

	var Custom = function() {
		return {
		}
	}();

	var DocumentOnResize = function() {
		return {
			init: function() {
				Core.viewport();
				Core.breakpoints();
				Base.menuBreakpoint();

				Core.run(vars.resizers);

				Custom.onResize();

				Core.addEvent( window, 'cnvsResize' );
			}
		};
	}();

	var DocumentOnReady = function() {
		return {
			init: function() {
				Core.breakpoints();
				Core.colorScheme();
				Core.runBase();
				Core.runModules();
				Core.topScrollOffset();

				if( vars.smoothScroll ) {
					new Core.smoothScroll();
				}

				DocumentOnReady.windowscroll();

				Custom.onReady();
			},

			windowscroll: function() {
				Core.scrollEnd( function() {
					Base.pageMenu();
				});
			}
		};
	}();

	var DocumentOnLoad = function() {
		return {
			init: function() {
				Custom.onLoad();
			}
		};
	}();

	document.addEventListener( 'DOMContentLoaded', function() {
		DocumentOnReady.init();
	});

	window.addEventListener('load', function() {
		DocumentOnLoad.init();
	});

	var resizeFunctions = Core.debouncedResize( function() {
		DocumentOnResize.init();
	}, 250);

	window.addEventListener('resize', function() {
		resizeFunctions();
	});

	var canvas_umd = {
		Core,
		Base,
		Modules,
		Mobile,
		Custom,
	};

	return canvas_umd;
})));

(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
	typeof define === 'function' && define.amd ? define(factory) :
	( global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.CNVS = factory() );
} (this, (function() {
	// USE STRICT
	"use strict";

	/**
	 * --------------------------------------------------------------------------
	 * DO NOT DELETE!! Start (Required)
	 * --------------------------------------------------------------------------
	 */
	if( SEMICOLON === 'undefined' || SEMICOLON.Core === 'undefined' || SEMICOLON.Base === 'undefined' || SEMICOLON.Modules === 'undefined' || SEMICOLON.Mobile === 'undefined' ) {
		return false;
	}

	var __core = SEMICOLON.Core;
	var __base = SEMICOLON.Base;
	var __modules = SEMICOLON.Modules;
	// DO NOT DELETE!! End

	return {
		

		/**
		 * --------------------------------------------------------------------------
		 * SliderDimension Functions Start (Required if using Sliders)
		 * --------------------------------------------------------------------------
		 */
		SliderDimensions: function() {
			return {
				init: function(selector) {
					selector = __core.getSelector( selector, false );
					if( selector.length < 1 ){
						return true;
					}

					var slider = document.querySelector('.slider-element'),
						sliderParallaxEl = document.querySelector('.slider-parallax'),
						body = __core.getVars.elBody,
						parallaxElHeight = sliderParallaxEl?.offsetHeight,
						parallaxElWidth = sliderParallaxEl?.offsetWidth,
						slInner = sliderParallaxEl?.querySelector('.slider-inner'),
						slSwiperW = slider.querySelector('.swiper-wrapper'),
						slSwiperS = slider.querySelector('.swiper-slide'),
						slFlexHeight = slider.classList.contains('h-auto') || slider.classList.contains('min-vh-0');

					if( body.classList.contains('device-up-lg') ) {
						setTimeout(function() {
							if( slInner ) {
								slInner.style.height = parallaxElHeight + 'px';
							}
							if( slFlexHeight ) {
								parallaxElHeight = slider.querySelector('.slider-inner')?.querySelector('*').offsetHeight;
								slider.style.height = parallaxElHeight + 'px';
								if( slInner ) {
									slInner.style.height = parallaxElHeight + 'px';
								}
							}
						}, 500);

						if( slFlexHeight && slSwiperS ) {
							var slSwiperFC = slSwiperS.querySelector('*');
							if( slSwiperFC.classList.contains('container') || slSwiperFC.classList.contains('container-fluid') ) {
								slSwiperFC = slSwiperFC.querySelector('*');
							}
							if( slSwiperFC.offsetHeight > slSwiperW.offsetHeight ) {
								slSwiperW.style.height = 'auto';
							}
						}

						if( body.classList.contains('side-header') && slInner ) {
							slInner.style.width = parallaxElWidth + 'px';
						}

						if( !body.classList.contains('stretched') ) {
							parallaxElWidth = __core.getVars.elWrapper.offsetWidth;
							if( slInner ) {
								slInner.style.width = parallaxElWidth + 'px';
							}
						}
					} else {
						if( slSwiperW ) {
							slSwiperW.style.height = '';
						}

						if( sliderParallaxEl ) {
							sliderParallaxEl.style.height = '';
						}

						if( slInner ) {
							slInner.style.width = '';
							slInner.style.height = '';
						}
					}

					__core.getVars.resizers.sliderdimensions = function() {
						__base.sliderDimensions();
					};
				}
			};
		}(),
		// SliderDimension Functions End


		/**
		 * --------------------------------------------------------------------------
		 * Animations Functions Start
		 * --------------------------------------------------------------------------
		 */
		Animations: function() {
			return {
				init: function(selector) {
					if( __core.getSelector(selector, false, false).length < 1 ){
						return true;
					}

					__core.initFunction({ class: 'has-plugin-animations', event: 'pluginAnimationsReady' });

					selector = __core.getSelector( selector, false );
					if( selector.length < 1 ){
						return true;
					}

					var SELECTOR = '[data-animate]',
						ANIMATE_CLASS_NAME = 'animated';

					var isAnimated = function(element) {
						element.classList.contains(ANIMATE_CLASS_NAME);
					};

					var intersectionObserver = new IntersectionObserver(
						function(entries, observer) {
							entries.forEach( function(entry) {
								var element = entry.target,
									elAnimation = element.getAttribute('data-animate'),
									elAnimOut = element.getAttribute('data-animate-out'),
									elAnimDelay = element.getAttribute('data-delay'),
									elAnimDelayOut = element.getAttribute('data-delay-out'),
									elAnimDelayTime = 0,
									elAnimDelayOutTime = 3000,
									elAnimations = elAnimation.split(' ');

								if( element.closest('.fslider.no-thumbs-animate') ) {
									return true;
								}

								if( element.closest('.swiper-slide') ) {
									return true;
								}

								if( elAnimDelay ) {
									elAnimDelayTime = Number( elAnimDelay ) + 500;
								} else {
									elAnimDelayTime = 500;
								}

								if( elAnimOut && elAnimDelayOut ) {
									elAnimDelayOutTime = Number( elAnimDelayOut ) + elAnimDelayTime;
								}

								if( !element.classList.contains('animated') ) {
									element.classList.add('not-animated');
									if( entry.intersectionRatio > 0 ) {
										setTimeout( function() {
											element.classList.remove('not-animated');
											elAnimations.forEach( function(item) {
												element.classList.add(item);
											});
											element.classList.add('animated');
										}, elAnimDelayTime);

										if( elAnimOut ) {
											setTimeout( function() {
												elAnimations.forEach( function(item) {
													element.classList.remove(item);
												});

												elAnimOut.split(' ').forEach( function(item) {
													element.classList.add(item);
												});
											}, elAnimDelayOutTime);
										}
									}
								}

								if( !element.classList.contains('not-animated') ) {
									observer.unobserve(element);
								}
							});
						}
					);

					var elements = [].filter.call(document.querySelectorAll(SELECTOR), function(element) {
						return !isAnimated(element, ANIMATE_CLASS_NAME);
					});

					elements.forEach( function(element) {
						return intersectionObserver.observe(element);
					});
				}
			};
		}(),
		// Animations Functions End
		
		/**
   * --------------------------------------------------------------------------
   * HoverAnimations Functions Start
   * --------------------------------------------------------------------------
   */
		 HoverAnimations: function() {
			var _t, _x;
		 
			var _showOverlay = function(params) {
			 clearTimeout(_x);
		 
			 _t = setTimeout( function() {
			  params.element.classList.add( 'not-animated' );
		 
			  (params.elAnimateOut + ' not-animated').split(" ").forEach( function(_class) {
			   params.element.classList.remove(_class);
			  });
		 
			  (params.elAnimate + ' animated').split(" ").forEach( function(_class) {
			   params.element.classList.add(_class);
			  });
			 }, params.elDelayT );
			};
		 
			var _hideOverlay = function(params) {
			 params.element.classList.add( 'not-animated' );
		 
			 (params.elAnimate + ' not-animated').split(" ").forEach( function(_class) {
			  params.element.classList.remove(_class);
			 });
		 
			 (params.elAnimateOut + ' animated').split(" ").forEach( function(_class) {
			  params.element.classList.add(_class);
			 });
		 
			 if( params.elReset == 'true' ) {
			  _x = setTimeout( function() {
			   (params.elAnimateOut + ' animated').split(" ").forEach( function(_class) {
				params.element.classList.remove(_class);
			   });
		 
			   params.element.classList.add( 'not-animated' );
			  }, Number( params.elSpeed ) );
			 }
		 
			 clearTimeout(_t);
			};
		 
			var _isInsideElement = function(touch){
			 var rect = element.getBoundingClientRect();
		 
			 return (
			  touch.clientX >= rect.left &&
			  touch.clientX <= rect.right &&
			  touch.clientY >= rect.top &&
			  touch.clientY <= rect.bottom
			 );
			};
		 
			return {
			 init: function(selector) {
			  if( __core.getSelector(selector, false, false).length < 1 ){
			   return true;
			  }
		 
			  __core.initFunction({ class: 'has-plugin-hoveranimation', event: 'pluginHoverAnimationReady' });
		 
			  selector = __core.getSelector( selector, false );
			  if( selector.length < 1 ){
			   return true;
			  }
		 
			  selector.forEach( function(element) {
			   var elAnimate = element.getAttribute( 'data-hover-animate' ),
				elAnimateOut = element.getAttribute( 'data-hover-animate-out' ) || 'fadeOut',
				elSpeed = element.getAttribute( 'data-hover-speed' ) || 600,
				elDelay = element.getAttribute( 'data-hover-delay' ),
				elParent = element.getAttribute( 'data-hover-parent' ),
				elReset = element.getAttribute( 'data-hover-reset' ) || 'false',
				elMobile = element.getAttribute( 'data-hover-mobile' ) || 'true';
		 
			   if( elMobile != 'true' ) {
				if( elMobile == 'false' ) {
				 if( !__core.getVars.elBody.classList.contains('device-up-lg') ) {
				  return true;
				 }
				} else {
				 if( !__core.getVars.elBody.classList.contains('device-up-' + elMobile) ) {
				  return true;
				 }
				}
			   }
		 
			   element.classList.add( 'not-animated' );
		 
			   if( !elParent ) {
				if( element.closest( '.bg-overlay' ) ) {
				 elParent = element.closest( '.bg-overlay' );
				} else {
				 elParent = element;
				}
			   } else {
				if( elParent == 'self' ) {
				 elParent = element;
				} else {
				 elParent = element.closest( elParent );
				}
			   }
		 
			   var elDelayT = 0;
		 
			   if( elDelay ) {
				elDelayT = Number( elDelay );
			   }
		 
			   if( elSpeed ) {
				element.style.animationDuration = Number( elSpeed ) + 'ms';
			   }
		 
			   var params = {
				element: element,
				elAnimate: elAnimate,
				elAnimateOut: elAnimateOut,
				elSpeed: elSpeed,
				elDelayT: elDelayT,
				elParent: elParent,
				elReset: elReset,
			   }
		 
			   elParent.addEventListener( 'mouseenter', function(){
				_showOverlay(params);
			   }, false);
		 
			   elParent.addEventListener( 'mouseleave', function(){
				_hideOverlay(params);
			   }, false);
		 
			   // elParent.addEventListener( 'touchstart', function(e){
			   //  e.preventDefault();
		 
			   //  _showOverlay(params);
			   //  elParent.addEventListener('touchmove', function(e){
				//   if (!_isInsideElement(e.touches[0])) {
				//    _hideOverlay(params);
				//    elParent.removeEventListener('touchmove');
				//   }
				//  });

				//  elParent.addEventListener('touchend', function(){
				//   _hideOverlay(params);
				//   elParent.removeEventListener('touchmove');
				//   elParent.removeEventListener('touchend');
				//  });
				// });
				});
				}
			};
			}(),
  // HoverAnimations Functions End
		/**
		 * --------------------------------------------------------------------------
		 * CanvasSlider Functions Start
		 * --------------------------------------------------------------------------
		 */
		CanvasSlider: function() {
			return {
				init: function(selector) {
					if( __core.getSelector(selector, false, false).length < 1 ){
						return true;
					}

					__core.isFuncTrue( function() {
						return typeof Swiper !== "undefined";
					}).then( function(cond) {
						if( !cond ) {
							return false;
						}

						__core.initFunction({ class: 'has-plugin-swiper', event: 'pluginSwiperReady' });

						selector = __core.getSelector( selector, false );
						if( selector.length < 1 ){
							return true;
						}

						selector.forEach( function(element) {
							if( !element.classList.contains('swiper_wrapper') ) {
								 return true;
							}

							if( element.querySelectorAll('.swiper-slide').length < 1 ) {
								return true;
							}

							var elDirection = element.getAttribute('data-direction') || 'horizontal',
								elSpeed = element.getAttribute('data-speed') || 300,
								elAutoPlay = element.getAttribute('data-autoplay'),
								elAutoPlayDisableOnInteraction = element.getAttribute('data-autoplay-disable-on-interaction') || true,
								elPauseOnHover = element.getAttribute('data-hover'),
								elLoop = element.getAttribute('data-loop'),
								elStart = element.getAttribute('data-start') || 1,
								elEffect = element.getAttribute('data-effect') || 'slide',
								elGrabCursor = element.getAttribute('data-grab'),
								elParallax = element.getAttribute('data-parallax'),
								elAutoHeight = element.getAttribute('data-autoheight'),
								slideNumberTotal = element.querySelector('.slide-number-total'),
								slideNumberCurrent = element.querySelector('.slide-number-current'),
								elVideoAutoPlay = element.getAttribute('data-video-autoplay'),
								elSettings = element.getAttribute('data-settings'),
								elPagination, elPaginationClickable;

							elAutoPlay = elAutoPlay ? Number( elAutoPlay ) : 999999999;
							elPauseOnHover = elPauseOnHover == 'true' ? true : false;
							elAutoPlayDisableOnInteraction = elAutoPlayDisableOnInteraction == 'false' ? false : true;
							elLoop = elLoop == 'true' ? true : false;
							elParallax = elParallax == 'true' ? true : false;
							elGrabCursor = elGrabCursor == 'false' ? false : true;
							elAutoHeight = elAutoHeight == 'true' ? true : false;
							elVideoAutoPlay = elVideoAutoPlay == 'false' ? false : true;
							elStart = elStart == 'random' ? Math.floor( Math.random() * element.querySelectorAll('.swiper-slide:not(.swiper-slide-duplicate)').length ) : Number( elStart ) - 1;

							if( element.querySelector('.swiper-pagination') ) {
								elPagination = element.querySelector('.swiper-pagination');
								elPaginationClickable = true;
							} else {
								elPagination = '';
								elPaginationClickable = false;
							}

							var elementNavNext = element.querySelector('.slider-arrow-right'),
								elementNavPrev = element.querySelector('.slider-arrow-left'),
								elementScollBar = element.querySelector('.swiper-scrollbar');

							var cnvsSwiper = new Swiper( element.querySelector('.swiper-parent'), {
								direction: elDirection,
								speed: Number( elSpeed ),
								autoplay: {
									delay: elAutoPlay,
									pauseOnMouseEnter: elPauseOnHover,
									disableOnInteraction: elAutoPlayDisableOnInteraction
								},
								loop: elLoop,
								initialSlide: elStart,
								effect: elEffect,
								parallax: elParallax,
								slidesPerView: 1,
								grabCursor: elGrabCursor,
								autoHeight: elAutoHeight,
								pagination: {
									el: elPagination,
									clickable: elPaginationClickable
								},
								navigation: {
									prevEl: elementNavPrev,
									nextEl: elementNavNext
								},
								scrollbar: {
									el: elementScollBar
								},
								on: {
									afterInit: function(swiper) {
										__base.sliderDimensions();

										if( element.querySelectorAll('.yt-bg-player').length > 0 ) {
											element.querySelectorAll('.yt-bg-player').forEach( function(el) {
												el.setAttribute('data-autoplay', 'false');
												el.classList.remove('customjs');
											});

											__modules.youtubeBgVideo();

											var activeYTVideo = jQuery('.swiper-slide-active').find('.yt-bg-player:not(.customjs)');
											activeYTVideo.on('YTPReady', function() {
												setTimeout( function() {
													activeYTVideo.filter('.mb_YTPlayer').YTPPlay();
												}, 1200);
											});
										}

										document.querySelectorAll('.swiper-slide-active [data-animate]').forEach( function(el) {
											var toAnimateDelay = el.getAttribute('data-delay'),
												toAnimateDelayTime = 0;

											if( toAnimateDelay ) {
												toAnimateDelayTime = Number( toAnimateDelay ) + 750;
											} else {
												toAnimateDelayTime = 750;
											}

											if( !el.classList.contains('animated') ) {
												el.classList.add('not-animated');

												var elementAnimation = el.getAttribute('data-animate');

												setTimeout( function() {
													el.classList.remove('not-animated');

													( elementAnimation + ' animated').split(" ").forEach( function(_class) {
														el.classList.add(_class);
													});
												}, toAnimateDelayTime);
											}
										});

										element.querySelectorAll('[data-animate]').forEach( function(el) {
											var elementAnimation = el.getAttribute('data-animate');

											if( el.closest('.swiper-slide').classList.contains('swiper-slide-active') ) {
												return true;
											}

											( elementAnimation + ' animated').split(" ").forEach( function(_class) {
												el.classList.remove(_class);
											});

											el.classList.add('not-animated');
										});

										if( elAutoHeight ) {
											setTimeout( function() {
												swiper.updateAutoHeight(300);
											}, 1000);
										}
									},
									transitionStart: function(swiper) {
										element.querySelectorAll('[data-animate]').forEach( function(el) {
											var elementAnimation = el.getAttribute('data-animate');

											if( el.closest('.swiper-slide').classList.contains('swiper-slide-active') ) {
												return true;
											}

											( elementAnimation + ' animated').split(" ").forEach( function(_class) {
												el.classList.remove(_class);
											});

											el.classList.add('not-animated');
										});

										SEMICOLON.Base.sliderMenuClass();
									},
									transitionEnd: function(swiper) {
										if( slideNumberCurrent ){
											if( elLoop == true ) {
												slideNumberCurrent.innerHTML = Number( element.querySelector('.swiper-slide.swiper-slide-active').getAttribute('data-swiper-slide-index') ) + 1;
											} else {
												slideNumberCurrent.innerHTML = swiper.activeIndex + 1;
											}
										}

										element.querySelectorAll('.swiper-slide').forEach( function(slide) {
											if( slide.querySelector('video') && elVideoAutoPlay == true ) {
												slide.querySelector('video').pause();
											}

											if( slide.querySelector('.yt-bg-player.mb_YTPlayer:not(.customjs)') ) {
												jQuery(slide).find('.yt-bg-player.mb_YTPlayer:not(.customjs)').YTPPause();
											}
										});

										element.querySelectorAll('.swiper-slide:not(.swiper-slide-active)').forEach( function(slide) {
											if( slide.querySelector('video') ) {
												if( slide.querySelector('video').currentTime != 0 ) {
													slide.querySelector('video').currentTime = 0;
												}
											}

											var activeYTPlayer = slide.querySelector('.yt-bg-player.mb_YTPlayer:not(.customjs)');

											if( activeYTPlayer ) {
												jQuery(activeYTPlayer).YTPSeekTo( activeYTPlayer.getAttribute('data-start') );
											}
										});

										if( element.querySelector('.swiper-slide.swiper-slide-active').querySelector('video') && elVideoAutoPlay == true ) {
											element.querySelector('.swiper-slide.swiper-slide-active').querySelector('video').play();
										}

										if( element.querySelector('.swiper-slide.swiper-slide-active').querySelector('.yt-bg-player.mb_YTPlayer:not(.customjs)') && elVideoAutoPlay == true ) {
											jQuery(element).find('.swiper-slide.swiper-slide-active').find('.yt-bg-player.mb_YTPlayer:not(.customjs)').YTPPlay();
										}

										element.querySelectorAll('.swiper-slide.swiper-slide-active [data-animate]').forEach( function(el) {
											var toAnimateDelay = el.getAttribute('data-delay'),
												toAnimateDelayTime = 0;

											if( toAnimateDelay ) {
												toAnimateDelayTime = Number( toAnimateDelay ) + 300;
											} else {
												toAnimateDelayTime = 300;
											}

											if( !el.classList.contains('animated') ) {
												el.classList.add('not-animated');

												var elementAnimation = el.getAttribute('data-animate');

												setTimeout( function() {
													el.classList.remove('not-animated');

													( elementAnimation + ' animated').split(" ").forEach( function(_class) {
														el.classList.add(_class);
													});
												}, toAnimateDelayTime);
											}
										});
									}
								}
							});

							if( slideNumberCurrent ) {
								if( elLoop == true ) {
									slideNumberCurrent.innerHTML = cnvsSwiper.realIndex + 1;
								} else {
									slideNumberCurrent.innerHTML = cnvsSwiper.activeIndex + 1;
								}
							}

							if( slideNumberTotal ) {
								slideNumberTotal.innerHTML = element.querySelectorAll('.swiper-slide:not(.swiper-slide-duplicate)').length;
							}
						});
					});
				}
			};
		}(),
		// CanvasSlider Functions End
	};
})));

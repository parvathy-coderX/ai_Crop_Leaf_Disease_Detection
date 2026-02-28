// Utility function to load Google Maps dynamically
export const loadGoogleMaps = (apiKey) => {
  return new Promise((resolve, reject) => {
    // If already loaded, resolve immediately
    if (window.google && window.google.maps) {
      console.log('Google Maps already loaded');
      resolve(window.google.maps);
      return;
    }

    // Check if script is already being loaded
    const existingScript = document.querySelector('script[src*="maps.googleapis"]');
    if (existingScript) {
      console.log('Google Maps script already loading');
      
      // Wait for it to load
      const checkInterval = setInterval(() => {
        if (window.google && window.google.maps) {
          clearInterval(checkInterval);
          resolve(window.google.maps);
        }
      }, 100);
      
      // Timeout after 10 seconds
      setTimeout(() => {
        clearInterval(checkInterval);
        reject(new Error('Google Maps load timeout'));
      }, 10000);
      
      return;
    }

    console.log('Loading Google Maps script...');
    
    // Create new script
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&callback=initMap`;
    script.async = true;
    script.defer = true;

    // Define callback function
    window.initMap = function() {
      console.log('Google Maps loaded successfully via callback');
      if (window.google && window.google.maps) {
        resolve(window.google.maps);
      } else {
        reject(new Error('Google Maps failed to initialize'));
      }
    };

    script.addEventListener('load', () => {
      console.log('Google Maps script loaded');
      // If callback hasn't fired yet, check manually
      if (window.google && window.google.maps) {
        resolve(window.google.maps);
      }
    });

    script.addEventListener('error', (error) => {
      console.error('Failed to load Google Maps script:', error);
      reject(new Error('Failed to load Google Maps script. Check your API key and network connection.'));
    });

    document.head.appendChild(script);
  });
};

// Alternative: If you want to use the js-api-loader package
// npm install @googlemaps/js-api-loader
export const loadGoogleMapsWithLoader = async (apiKey) => {
  try {
    const { Loader } = await import('@googlemaps/js-api-loader');
    
    const loader = new Loader({
      apiKey: apiKey,
      version: 'weekly',
      libraries: ['places']
    });

    const google = await loader.load();
    return google.maps;
  } catch (error) {
    console.error('Error loading Google Maps with loader:', error);
    throw error;
  }
};
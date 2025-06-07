"""
Test suite for Flask + Pyodide + HTMX + Tailwind CSS v4 project setup.

This test suite verifies that all components are properly configured and working.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
import pytest
from bs4 import BeautifulSoup


class TestProjectStructure:
    """Test that all required files and directories exist."""
    
    def test_required_files_exist(self):
        """Test that all essential project files exist."""
        required_files = [
            "index.html",
            "main.py", 
            "style.css",
            "static/style.css",
            "package.json",
            "requirements.txt",
            "README.md",
            ".gitignore"
        ]
        
        for file_path in required_files:
            assert Path(file_path).exists(), f"Required file {file_path} is missing"
    
    def test_static_directory_exists(self):
        """Test that static directory exists."""
        assert Path("static").is_dir(), "Static directory should exist"
    
    def test_node_modules_exists(self):
        """Test that node_modules directory exists (dependencies installed)."""
        assert Path("node_modules").is_dir(), "node_modules directory should exist after npm install"


class TestPythonEnvironment:
    """Test Python environment and dependencies."""
    
    def test_python_dependencies_installed(self):
        """Test that required Python packages are installed."""
        try:
            import flask
            import pycardano
        except ImportError as e:
            pytest.fail(f"Required Python dependency not installed: {e}")
    
    def test_flask_app_importable(self):
        """Test that the Flask app can be imported without errors."""
        try:
            # Add current directory to path to import main
            sys.path.insert(0, str(Path.cwd()))
            import main
            assert hasattr(main, 'app'), "Flask app should be defined in main.py"
            assert main.app is not None, "Flask app should not be None"
        except Exception as e:
            pytest.fail(f"Failed to import Flask app: {e}")
        finally:
            # Clean up
            if 'main' in sys.modules:
                del sys.modules['main']
            if str(Path.cwd()) in sys.path:
                sys.path.remove(str(Path.cwd()))
    
    def test_requirements_file_format(self):
        """Test that requirements.txt is properly formatted."""
        req_file = Path("requirements.txt")
        assert req_file.exists(), "requirements.txt should exist"
        
        content = req_file.read_text()
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Should have some dependencies
        assert len(lines) > 0, "requirements.txt should not be empty"
        
        # Check for key dependencies
        dep_names = [line.split('==')[0].lower() for line in lines]
        assert 'flask' in dep_names, "Flask should be in requirements.txt"
        assert 'pycardano' in dep_names, "PyCardano should be in requirements.txt"


class TestNodeJSEnvironment:
    """Test Node.js environment and dependencies."""
    
    def test_package_json_structure(self):
        """Test that package.json has correct structure."""
        with open("package.json", "r") as f:
            package = json.load(f)
        
        assert "scripts" in package, "package.json should have scripts section"
        assert "build" in package["scripts"], "Should have build script"
        assert "dev" in package["scripts"], "Should have dev script"
        
        # Check for Tailwind dependencies
        deps = package.get("dependencies", {})
        dev_deps = package.get("devDependencies", {})
        all_deps = {**deps, **dev_deps}
        
        assert "tailwindcss" in all_deps, "tailwindcss should be in dependencies"
        assert "@tailwindcss/cli" in all_deps, "@tailwindcss/cli should be in dependencies"
    
    def test_tailwind_cli_available(self):
        """Test that Tailwind CLI is available and working."""
        try:
            result = subprocess.run(
                ["npx", "@tailwindcss/cli", "--help"],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0, "Tailwind CLI should be available"
            assert "tailwindcss" in result.stdout.lower(), "Should show Tailwind CLI help"
        except subprocess.TimeoutExpired:
            pytest.fail("Tailwind CLI command timed out")


class TestTailwindCSS:
    """Test Tailwind CSS v4 setup and functionality."""
    
    def test_style_css_import_format(self):
        """Test that style.css uses the correct v4 import format."""
        content = Path("style.css").read_text()
        assert '@import "tailwindcss";' in content, "style.css should use v4 import format"
        assert "@tailwind" not in content, "style.css should not use old v3 directives"
    
    def test_css_build_works(self):
        """Test that CSS can be built successfully."""
        # Run Tailwind build command
        result = subprocess.run(
            ["npx", "@tailwindcss/cli", "-i", "./style.css", "-o", "./static/test-style.css"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        assert result.returncode == 0, f"CSS build should succeed. Error: {result.stderr}"
        
        # Clean up test file
        test_file = Path("static/test-style.css")
        if test_file.exists():
            test_file.unlink()
    
    def test_generated_css_content(self):
        """Test that generated CSS has expected Tailwind v4 features."""
        css_file = Path("static/style.css")
        assert css_file.exists(), "Generated CSS file should exist"
        
        content = css_file.read_text()
        
        # Check for v4 features
        assert "@layer" in content, "Should use CSS cascade layers"
        assert "tailwindcss v4" in content, "Should indicate v4 in header comment"
        assert "--color-" in content, "Should contain CSS custom properties for colors"
        assert "oklch(" in content, "Should use OKLCH color format"
        
        # Check for utility classes used in our HTML
        assert ".text-4xl" in content, "Should include text-4xl utility"
        assert ".font-bold" in content, "Should include font-bold utility"
        assert ".text-blue-600" in content, "Should include text-blue-600 utility"


class TestHTMLStructure:
    """Test HTML file structure and content."""
    
    def test_html_file_valid(self):
        """Test that index.html is valid and well-formed."""
        with open("index.html", "r") as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Basic HTML structure
        assert soup.html is not None, "Should have html tag"
        assert soup.head is not None, "Should have head tag"
        assert soup.body is not None, "Should have body tag"
        
        # Required meta tags
        charset_meta = soup.find("meta", {"charset": True})
        assert charset_meta is not None, "Should have charset meta tag"
        
        viewport_meta = soup.find("meta", {"name": "viewport"})
        assert viewport_meta is not None, "Should have viewport meta tag"
    
    def test_css_link_correct(self):
        """Test that HTML links to the correct CSS file."""
        with open("index.html", "r") as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        css_link = soup.find("link", {"rel": "stylesheet"})
        
        assert css_link is not None, "Should have CSS link tag"
        assert css_link.get("href") == "./static/style.css", "Should link to correct CSS file"
    
    def test_htmx_and_hyperscript_loaded(self):
        """Test that HTMX and Hyperscript are properly loaded."""
        with open("index.html", "r") as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        scripts = soup.find_all("script", {"src": True})
        
        htmx_loaded = any("htmx" in script.get("src", "").lower() for script in scripts)
        hyperscript_loaded = any("hyperscript" in script.get("src", "").lower() for script in scripts)
        
        assert htmx_loaded, "HTMX should be loaded"
        assert hyperscript_loaded, "Hyperscript should be loaded"
    
    def test_pyodide_setup(self):
        """Test that Pyodide is properly configured."""
        with open("index.html", "r") as f:
            content = f.read()
        
        # Check for Pyodide import
        assert "pyodide" in content.lower(), "Should reference Pyodide"
        assert "loadPyodide" in content, "Should call loadPyodide function"
        
        # Check for main.py fetch
        assert "main.py" in content, "Should fetch main.py file"
    
    def test_tailwind_classes_used(self):
        """Test that HTML uses Tailwind CSS classes."""
        with open("index.html", "r") as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find elements with class attributes
        elements_with_classes = soup.find_all(attrs={"class": True})
        assert len(elements_with_classes) > 0, "Should have elements with CSS classes"
        
        # Check for common Tailwind patterns
        all_classes = " ".join([" ".join(el.get("class", [])) for el in elements_with_classes])
        
        tailwind_patterns = ["text-", "bg-", "p-", "m-", "font-", "hover:"]
        tailwind_found = any(pattern in all_classes for pattern in tailwind_patterns)
        assert tailwind_found, "Should use Tailwind CSS utility classes"


class TestGitIgnore:
    """Test .gitignore file."""
    
    def test_gitignore_covers_essentials(self):
        """Test that .gitignore covers essential patterns."""
        content = Path(".gitignore").read_text()
        
        essential_patterns = [
            "node_modules/",
            ".venv/",
            "__pycache__/",
            ".DS_Store",
            "*.log"
        ]
        
        for pattern in essential_patterns:
            assert pattern in content, f".gitignore should include {pattern}"


class TestDocumentation:
    """Test project documentation."""
    
    def test_readme_has_required_sections(self):
        """Test that README has all required sections."""
        content = Path("README.md").read_text()
        
        required_sections = [
            "setup",
            "development", 
            "run"
        ]
        
        content_lower = content.lower()
        for section in required_sections:
            assert f"## {section}" in content_lower, f"README should have {section} section"
    
    def test_readme_has_correct_commands(self):
        """Test that README contains correct setup commands."""
        content = Path("README.md").read_text()
        
        # Should mention the correct commands
        assert "npm run dev" in content, "README should mention npm run dev"
        assert "npm run build" in content, "README should mention npm run build"
        assert "uv venv" in content, "README should mention uv venv"


class TestPyCardanoIntegration:
    """Test PyCardano integration and functionality."""
    
    def test_pycardano_imports(self):
        """Test that PyCardano can be imported and key classes are available."""
        try:
            from pycardano import PaymentKeyPair, Address, Network
            
            # Test that key classes exist and are callable
            assert callable(PaymentKeyPair.generate), "PaymentKeyPair.generate should be callable"
            assert hasattr(Address, '__init__'), "Address should be instantiable"
            assert hasattr(Network, 'TESTNET'), "Network should have TESTNET attribute"
            assert hasattr(Network, 'MAINNET'), "Network should have MAINNET attribute"
            
        except ImportError as e:
            pytest.fail(f"Failed to import PyCardano components: {e}")
    
    def test_address_generation_functionality(self):
        """Test that address generation works correctly."""
        try:
            from pycardano import PaymentKeyPair, Address, Network
            
            # Generate a key pair
            key_pair = PaymentKeyPair.generate()
            assert key_pair is not None, "Key pair generation should succeed"
            assert hasattr(key_pair, 'verification_key'), "Key pair should have verification_key"
            assert hasattr(key_pair, 'signing_key'), "Key pair should have signing_key"
            
            # Generate testnet address
            testnet_address = Address(key_pair.verification_key.hash(), network=Network.TESTNET)
            assert testnet_address is not None, "Testnet address generation should succeed"
            
            testnet_str = str(testnet_address)
            assert testnet_str.startswith('addr_test'), "Testnet address should start with 'addr_test'"
            assert len(testnet_str) > 50, "Address should be reasonably long"
            
            # Generate mainnet address for comparison
            mainnet_address = Address(key_pair.verification_key.hash(), network=Network.MAINNET)
            mainnet_str = str(mainnet_address)
            assert mainnet_str.startswith('addr1'), "Mainnet address should start with 'addr1'"
            
            # Addresses should be different
            assert testnet_str != mainnet_str, "Testnet and mainnet addresses should differ"
            
        except Exception as e:
            pytest.fail(f"Address generation failed: {e}")
    
    def test_flask_pycardano_route_exists(self):
        """Test that the PyCardano Flask route is properly defined."""
        try:
            sys.path.insert(0, str(Path.cwd()))
            import main
            
            # Test that the route exists
            with main.app.test_client() as client:
                response = client.get('/pycardano')
                
                # Should not return 404
                assert response.status_code != 404, "PyCardano route should exist"
                
                # Should return valid response (200 or handled error)
                assert response.status_code in [200, 500], f"Unexpected status code: {response.status_code}"
                
                if response.status_code == 200:
                    # Should return JSON
                    assert response.content_type == 'application/json', "Should return JSON content"
                    
                    # Parse JSON response
                    data = response.get_json()
                    assert 'address' in data, "Response should contain 'address' field"
                    
                    address = data['address']
                    assert isinstance(address, str), "Address should be a string"
                    assert address.startswith('addr_test'), "Should return testnet address"
                    assert len(address) > 50, "Address should be valid length"
                
        except Exception as e:
            pytest.fail(f"Flask PyCardano route test failed: {e}")
        finally:
            # Clean up
            if 'main' in sys.modules:
                del sys.modules['main']
            if str(Path.cwd()) in sys.path:
                sys.path.remove(str(Path.cwd()))
    
    def test_multiple_address_generation_uniqueness(self):
        """Test that multiple address generations produce unique addresses."""
        try:
            sys.path.insert(0, str(Path.cwd()))
            import main
            
            addresses = set()
            
            with main.app.test_client() as client:
                # Generate multiple addresses
                for _ in range(5):
                    response = client.get('/pycardano')
                    assert response.status_code == 200, "Each request should succeed"
                    
                    data = response.get_json()
                    address = data['address']
                    addresses.add(address)
                
                # All addresses should be unique (since we generate new key pairs each time)
                assert len(addresses) == 5, "All generated addresses should be unique"
                
                # All should be valid testnet addresses
                for address in addresses:
                    assert address.startswith('addr_test'), f"Invalid address format: {address}"
                
        except Exception as e:
            pytest.fail(f"Multiple address generation test failed: {e}")
        finally:
            # Clean up
            if 'main' in sys.modules:
                del sys.modules['main']
            if str(Path.cwd()) in sys.path:
                sys.path.remove(str(Path.cwd()))
    
    def test_pycardano_dependencies_compatibility(self):
        """Test that PyCardano dependencies are compatible with the project."""
        try:
            # Test that all PyCardano dependencies can be imported
            import cbor2
            import cryptography
            import pydantic
            import nacl
            
            # Test basic functionality of key dependencies
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.backends import default_backend
            
            # Test CBOR functionality (used in Cardano)
            test_data = {"test": "data", "number": 42}
            encoded = cbor2.dumps(test_data)
            decoded = cbor2.loads(encoded)
            assert decoded == test_data, "CBOR encoding/decoding should work"
            
        except ImportError as e:
            pytest.fail(f"PyCardano dependency import failed: {e}")
        except Exception as e:
            pytest.fail(f"PyCardano dependency functionality test failed: {e}")
    
    def test_html_pycardano_button_exists(self):
        """Test that the HTML contains the PyCardano button and output elements."""
        with open("index.html", "r") as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Test for PyCardano section
        pycardano_section = soup.find("h2", string=lambda text: text and "pycardano" in text.lower())
        assert pycardano_section is not None, "Should have PyCardano section heading"
        
        # Test for Generate Address button
        generate_button = soup.find("button", string=lambda text: text and "generate address" in text.lower())
        assert generate_button is not None, "Should have Generate Address button"
        
        # Test button has correct HTMX attributes
        assert generate_button.get("hx-get") == "/pycardano", "Button should call /pycardano endpoint"
        assert generate_button.get("hx-target") == "#pycardano-output", "Button should target output div"
        
        # Test for output div
        output_div = soup.find("div", {"id": "pycardano-output"})
        assert output_div is not None, "Should have pycardano-output div"
        assert "font-mono" in output_div.get("class", []), "Output should use monospace font"
        
    def test_service_worker_handles_pycardano_route(self):
        """Test that the service worker is configured to handle the PyCardano route."""
        with open("sw.js", "r") as f:
            content = f.read()
        
        # Should not hard-code specific routes anymore (generic solution)
        assert "staticFileExtensions" in content, "Should use generic file extension checking"
        assert "hasFileExtension" in content, "Should check for file extensions"
        
        # Should handle any non-static route
        assert "handleFlaskRequest" in content, "Should have Flask request handler"
        
        # Should have fallback mechanism
        assert "fall back" in content.lower() or "fallback" in content.lower(), "Should have fallback handling"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"]) 
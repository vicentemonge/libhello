from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import get
from conan.tools.scm import Git
from conan.tools.files import update_conandata


class helloRecipe(ConanFile):
    name = "hello"
    version = "1.0"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of hello package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def export(self):
        git = Git(self, self.recipe_folder)
        scm_url, scm_commit = git.get_url_and_commit()
        self.output.info(f"Obtained URL: {scm_url} and {scm_commit}")
        # we store the current url and commit in conandata.yml
        update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

    def source(self):
        # we recover the saved url and commit from conandata.yml and use them to get sources
        git = Git(self)
        sources = self.conan_data["sources"]
        self.output.info(f"Cloning sources from: {sources}")
        git.clone(url=sources["url"], target=".")
        git.checkout(commit=sources["commit"])

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["hello"]

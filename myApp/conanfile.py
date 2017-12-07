from conans import ConanFile, tools

class App(ConanFile):
    name = "myApp"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    requires = "libA/0.1@conan/testing"

    generators = "visual_studio"

    repo_base_path = "file:///cygdrive/c/Users/kostja/Dev/conan-example-shared"

    def source(self):
        self.run("git archive --remote %s -- HEAD %s | tar x" % (self.repo_base_path, self.name))

    def build(self):
        path_to_solution = "%s\\%s\\%s.sln" % (self.source_folder, self.name, self.name)
        build_command = tools.build_sln_command(self.settings, path_to_solution)
        command = "%s && %s" % (tools.vcvars_command(self.settings), build_command)

    def package(self):
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.exe", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self.name]

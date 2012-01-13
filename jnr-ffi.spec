%global git_commit 103ea1a
%global cluster jnr

Name:     jnr-ffi
Version:  0.5.10
Release:  4%{?dist}
Summary:  Java Abstracted Foreign Function Layer
Group:    System Environment/Libraries
License:  ASL 2.0 or LGPLv3+
URL:      http://github.com/%{cluster}/%{name}
Source0:  https://download.github.com/%{cluster}-%{name}-%{version}-0-g%{git_commit}.tar.gz
Patch0:   jaffl_fix_jar_dependencies.patch

# invokedynamic is a Java 7 feature and the method
# which needs it is only defined and not used
Patch1:   jaffl_remove_invokedynamic.patch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: jffi
BuildRequires: jnr-x86asm
BuildRequires: objectweb-asm

Requires:      java
Requires:      jpackage-utils
Requires:      jffi
Requires:      jnr-x86asm
Requires:      objectweb-asm
BuildArch:     noarch

Obsoletes: jaffl < %{version}-%{release}
Provides:  jaffl = %{version}-%{release}

%description
An abstracted interface to invoking native functions from java

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{cluster}-%{name}-%{git_commit}
%patch0 -p0
%patch1 -p0

# remove all builtin jars
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;

# remove tests/junit dependency
rm -rf test/

mkdir build_lib
build-jar-repository -s -p build_lib jffi jnr-x86asm objectweb-asm/asm \
                                     objectweb-asm/analysis objectweb-asm/commons \
                                     objectweb-asm/tree objectweb-asm/util objectweb-asm/xml

%build
ant

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}

cp dist/jaffl-0.5.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{_javadir}/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/jaffl.jar

cp -rp dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# pom
%add_to_maven_depmap org.jruby.extras %{name} %{version} JPP %{name}
mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
cp pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-jnr-ffi.pom

#%add_maven_depmap JPP-jnr-ffi.pom jnr-ffi.jar


%files
%{_javadir}/jaffl.jar
%{_javadir}/%{name}.jar
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*
%doc LICENSE

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-3
- more updates to conform to fedora guidelines

* Wed Aug 10 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-2
- updated to conform to fedora guidelines

* Tue Aug 02 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-1
- initial package

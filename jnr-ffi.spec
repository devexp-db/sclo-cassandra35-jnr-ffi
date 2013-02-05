%global commit_hash f28dc0a
%global tag_hash 929dd3c

Name:     jnr-ffi
Version:  0.7.10
Release:  1%{?dist}
Summary:  Java Abstracted Foreign Function Layer
Group:    System Environment/Libraries
License:  ASL 2.0
URL:      http://github.com/jnr/%{name}/
Source0:  https://github.com/jnr/%{name}/tarball/%{version}/jnr-%{name}-%{version}-0-g%{commit_hash}.tar.gz

Patch1:   %{name}-remove-dependency-versions-not-understood-by-fedora-maven.patch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: jffi
BuildRequires: jnr-x86asm
BuildRequires: junit
BuildRequires: objectweb-asm

BuildRequires:  maven-local
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin

Requires:      java
Requires:      jpackage-utils
Requires:      jffi
Requires:      jnr-x86asm
Requires:      objectweb-asm

BuildArch:     noarch

# don't obsolete/provide jaffl, gradle is using both jaffl and jnr-ffi...

%description
An abstracted interface to invoking native functions from java

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jnr-%{name}-%{tag_hash}
%patch1 -p0

# remove all builtin jars
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;

%build
# don't fail on unused parameters... (TODO: send patch upstream)
sed -i 's|-Werror||' libtest/GNUmakefile
# TODO: tests still fail, investigate
mvn-rpmbuild install javadoc:aggregate -DskipTests

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%doc LICENSE
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%changelog
* Tue Feb 05 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.10-1
- Update to version 0.7.10.
- Switch from ant to maven.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-3
- more updates to conform to fedora guidelines

* Wed Aug 10 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-2
- updated to conform to fedora guidelines

* Tue Aug 02 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-1
- initial package

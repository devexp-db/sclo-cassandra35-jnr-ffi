Name:     jnr-ffi
Version:  2.0.2
Release:  1%{?dist}
Summary:  Java Abstracted Foreign Function Layer
License:  ASL 2.0
URL:      http://github.com/jnr/%{name}/
Source0:  https://github.com/jnr/%{name}/archive/%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(com.github.jnr:jffi)
BuildRequires:  mvn(com.github.jnr:jffi::native:)
BuildRequires:  mvn(com.github.jnr:jnr-x86asm)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-analysis)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(org.ow2.asm:asm-tree)
BuildRequires:  mvn(org.ow2.asm:asm-util)
BuildRequires:  sonatype-oss-parent


BuildArch:     noarch

# don't obsolete/provide jaffl, gradle is using both jaffl and jnr-ffi...

%description
An abstracted interface to invoking native functions from java

%package javadoc
Summary:        Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

# remove all builtin jars
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;

# don't fail on unused parameters... (TODO: send patch upstream)
sed -i 's|-Werror||' libtest/GNUmakefile

%mvn_file :{*} %{name}/@1 @1

%build
# skip tests on arm: https://bugzilla.redhat.com/show_bug.cgi?id=991712
%ifnarch %{arm}
%mvn_build
%else
%mvn_build -f
%endif

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Thu Apr 30 2015 Alexander Kurtakov <akurtako@redhat.com> 2.0.2-1
- Update to upstream 2.0.2.

* Thu Feb 19 2015 Michal Srb <msrb@redhat.com> - 2.0.1-3
- Skip tests on arm

* Wed Feb 18 2015 Michal Srb <msrb@redhat.com> - 2.0.1-2
- Build with jffi-native

* Mon Jan 05 2015 Mo Morsi <mmorsi@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 25 2013 Michal Srb <msrb@redhat.com> - 0.7.10-4
- Adapt to current guidelines
- Remove unneeded patch
- Enable tests
- Fix BR

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.10-2
- Depend on objectweb-asm4, not objectweb-asm.

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

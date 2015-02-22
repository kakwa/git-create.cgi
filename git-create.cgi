#!/usr/bin/perl -w

BEGIN {
# make the environment safe
  delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
  $ENV{PATH} = "";
}

use strict;
use CGI;
#use Path::Class qw(file);
use CGI::Carp qw(fatalsToBrowser);
#use Apache::Htpasswd;
my $cgi = new CGI;
$|++;

my %settings = (title    => "Git Creation Page",
                gitdir   => "/var/www/git/",
                gitcmd   => "/usr/bin/git",
                withtrac => "true",
		gitalias => "gitdir",
                traccmd  => "/usr/bin/trac-admin",
                tracdir  => "/var/www/trac/",
                fields   => [ "newgitname", "newgitdesc" ],
               );
$settings{user} = $ENV{REMOTE_USER};

if ( $ENV{GITDIR} ){
   $settings{gitdir} = $ENV{GITDIR};
}
if ( $ENV{GITCMD} ){
   $settings{gitcmd} = $ENV{GITCMD};
}
if ( $ENV{WITHTRAC} ){
   $settings{withtrac} = $ENV{WITHTRAC};
}
if ( $ENV{TRACCMD} ){
   $settings{traccmd} = $ENV{TRACCMD};
}
if ( $ENV{TRACDIR} ){
   $settings{tracdir} = $ENV{TRACDIR};
}
if ( $ENV{GITALIAS} ){
   $settings{gitalias} = $ENV{GITALIAS};
}

our $proto = 'http://';
if ( $ENV{HTTPS} eq 'on' ){
  $proto = 'https://';
}

#$settings{gitdir} =~ s%$ENV{DOCUMENT_ROOT}%% ;
#my $abspath = file $settings{gitdir};
my $gitpath = $settings{gitalias};

if ($ENV{REQUEST_METHOD} eq 'GET'){
  print_page_headers();
  print_form();
  print_git_repos();
  print_end();
}
if ($ENV{REQUEST_METHOD} eq 'POST'){
  print_page_headers();
  process_form();
  return_link();
#  print_header();
  print_end();
}


sub process_form{
  return;
}

sub return_link{
  
  return;
}

# print page header
sub print_page_headers {
  my $title = $settings{title} || "Page without a title";
  print $cgi->header(-charset => 'utf-8');
  print $cgi->start_html($title);
  print $cgi->h2($title);
  print $cgi->hr();
  return;
}


# scan the git root directory for git repository
sub print_git_repos {
  my $gitdir = $settings{gitdir} || die "Missing GIT Directory Parameter";
  print $cgi->h3("Existing Git Repositories");
  print $cgi->hr();
  print $cgi->start_table({-border=>1});
  print $cgi->Tr(
	 $cgi->th(['Name', 'URL', 'Description'])
  );
  opendir(my $dh, $settings{gitdir}) || die;
  #foreach my $dir (sort { -d $a <=> -d $b } readdir($dh)) {
  while(readdir $dh) {
    my $dir = $_;
    my $desc = '';
    if ( -f "$settings{gitdir}/$dir/config"){
      if( -f "$settings{gitdir}/$dir/description"){
        open(fh, "$settings{gitdir}/$dir/description");
        $desc = <fh>;
      }
      print $cgi->Tr(
          $cgi->td([$dir, "${proto}$ENV{SERVER_NAME}/${gitpath}/${dir}", "${desc}"])
      );
    }
  }
  print $cgi->end_table();
  print $cgi->hr();
  return; 
}

# Form to create a new git repository
sub print_form {
  for (@{$settings{fields}} ){
    $cgi->delete($_);
  } 
  print $cgi->h3("Create a new git repository");
  print $cgi->hr();
  print $cgi->start_form();
  print $cgi->table({-border=>0},
  $cgi->Tr($cgi->td('New Git Name:'),
  $cgi->td($cgi->textfield(-name      => 'newgitname',
                           -value     => '',
                           -size      => 20,
                           -maxlength => 18)),),
  $cgi->Tr($cgi->td('New Git Description:'),
  $cgi->td($cgi->textfield(-name      => 'newgitdesc',
                           -value     => '',
                           -size      => 80,
                           -maxlength => 78)),),
  $cgi->Tr($cgi->td($cgi->submit(-name  => 'gitcreate',
                                 -value => 'Create Git'))),);
  print $cgi->end_form(), $cgi->hr();
}

# print end of the page
sub print_end {
  print $cgi->end_html();
  return;
}

# small function printing all http headers
sub print_header {
  print $cgi->h3("HTTP Headers");
  foreach(sort keys %ENV) {
  print "<table>";
  print "<tr>
    <td >$_</td>
    <td ><tt>$ENV{$_}</tt></td>
    <td ></tr>";
  print "</table>";
  }
  print $cgi->hr();
}

exit;

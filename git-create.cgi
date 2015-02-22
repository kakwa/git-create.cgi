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


my $color = $cgi->param("color") || "#e1e5ff";
my $css = <<EOT;
body{
background:$color;
font-family:sans-serif;
font-size:11pt;
padding:0;
margin:0;
}
#content{
background:#fff;
padding:10px;
margin:0 5%;
}
#menu{
text-align:center;
margin-top:30px;
}
a{
text-decoration:none;
font-weight:bold;
}
h1{
font-size:16pt;
text-align:center;
margin:5px 100px;
border:2px solid $color;
}
h2{
border-bottom:2px solid $color;
}
p.note{
border:1px solid #ccc;
padding:5px;
background:#eee;
}
table{
border:1px solid #ccc;
border-collapse:collapse;
margin:5px 0;
width:100%;
font-size:small;
}
tr{
border:1px dotted #ccc;
}
tr:hover{
background:#eee;
}
th{
background:#eee;
}
td, th{
padding:3px 5px;
}
td.emphase{
background-color:#eee;
font-weight:bold;
}
ul {
list-style-type:none;
}
EOT

my %settings = (title    => "Git Creation Page",
                gitdir   => "/var/www/git/",
                gitcmd   => "/usr/bin/git",
                withtrac => "false",
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
  print_end();
}

sub fail{
  print "$_";
  exit 1;
}

sub process_form{
  my %data;
  for my $field ($cgi->param()){
    if ( scalar grep /^\Q$field\E$/, @{$settings{fields}} ){
      # its a field we know about
      my $tmp = substr($cgi->param($field), 0, 50);
      $tmp = lc($tmp) if ( $field eq "change_user_name" );
      $data{$field} = $tmp || '';
    }
  }
  if ( "$data{newgitname}" eq ''){
    print "Missing New Git Name.";
    return;
  }
  if ( $data{newgitname} =~ m/^\..*/ 
	or $data{newgitname} =~ m/.*\/.*/ 
	or  $data{newgitname} =~ m/.*\ .*/) {
    print "Forbidden character in new Git name.";
    return;
  }

  if ( -d "$settings{gitdir}/$data{newgitname}/" ){
    print "Git repository '$data{newgitname}' already exists.";
    return;
  }

  mkdir "$settings{gitdir}/$data{newgitname}/" or die $!;
  chdir "$settings{gitdir}/$data{newgitname}/" or die $!;
  system("$settings{gitcmd} init --bare") and die $!;
  system("$settings{gitcmd} update-server-info") and die $!;
  
  open(my $fh, '>', "$settings{gitdir}/$data{newgitname}/description") or die $!;
  print $fh "$data{newgitdesc}" or die $!;
  close $fh;
  
  if ($settings{withtrac} eq 'true'){
    system("$settings{traccmd} '$settings{tracdir}' repository add '$data{newgitname}' '$settings{gitdir}/$data{newgitname}/' git") and die $!;
    system("$settings{traccmd} '$settings{tracdir}' repository set '$data{newgitname}' description '$data{newgitdesc}'") and die $!;

  }
  return;
}

sub return_link{
  print "<br><a href=\"$ENV{URI}\">Return</a>";
  
  return;
}

# print page header
sub print_page_headers {
  my $title = $settings{title} || "Page without a title";
  print $cgi->header(-charset => 'utf-8');
  print $cgi->start_html( -title => "$title",
	 -style => { -code => $css });
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
  opendir(dh, $settings{gitdir}) || die;
  my @gitrepo = readdir(dh);
  @gitrepo = sort @gitrepo;
  while( my $dir = shift @gitrepo ) {
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

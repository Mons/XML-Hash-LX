use 5.006002;
use strict;
use warnings;
use Benchmark::Isolated;
use lib::abs ();

sub hash2xml($;%);

sub test {
	hash2xml( { node => [ { -attr => "test" }, { sub => 'test' }, { tx => { '#text' => ' zzzz ' } } ] } );
	hash2xml( { node => [ { _attr => "test" }, { sub => 'test' }, { tx => { '#text' => 'zzzz' } } ] }, attr => '_' );
	hash2xml( { node => [ { -attr => "test" }, { sub => 'test' }, { tx => { '~' => 'zzzz' } } ] }, text => '~' );
	hash2xml( { node => { sub => [ " \t\n", 'test' ] } }, trim => 1 );
	hash2xml( { node => { sub => [ " \t\n", 'test' ] } }, trim => 0 );
	hash2xml( { node => { sub => { '@' => 'test' } } }, cdata => '@' );
	hash2xml( { node => { sub => { '/' => 'test' } } },comm => '/' );
	hash2xml( { node => { -attr => undef, '#cdata' => undef, '/' => undef, x=>undef } }, cdata => '#cdata', comm => '/' );
}

cmpthese timethose -10, {
	old => sub {
		lib::abs->import('lib');
		require XML::Hash::LX;
		XML::Hash::LX->import();
		print "old = $XML::Hash::LX::VERSION\n";
		*hash2xml = \&XML::Hash::LX::hash2xml;
		return \&test;
	},
	new => sub {
		lib::abs->import('../lib');
		require XML::Hash::LX;
		XML::Hash::LX->import();
		print "new = $XML::Hash::LX::VERSION\n";
		*hash2xml = \&XML::Hash::LX::hash2xml;
		return \&test;
	},
}

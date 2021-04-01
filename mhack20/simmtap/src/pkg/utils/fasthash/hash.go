package fasthash

import (
	"bytes"
	"encoding/binary"
	"encoding/hex"
)

type FastHash struct {
	state  []uint32
	buffer []byte
	round  int
}

func New() *FastHash {
	return &FastHash{
		state: []uint32{3512596791, 1737493841, 4222670653, 2170878537, 2866504349, 2603312223, 1250887207, 2823867643, 1080138741, 2928425207, 4270571529, 3720532451, 3907612629, 2205910373, 2372223117, 4112017799},
		round: 0,
	}
}

func (f *FastHash) Update(buf []byte) {
	f.buffer = append(f.buffer, buf...)
	for len(f.buffer) > 4 {
		f.doRound()
	}
}

func (f *FastHash) Digest() []byte {
	tmpf := f.copy()
	for len(tmpf.buffer) < 4 {
		tmpf.buffer = append(tmpf.buffer, byte(0xff))
	}
	tmpf.doRound()
	digest := new(bytes.Buffer)
	var digestblock uint32
	for i := 0; i < 4; i++ {
		digestblock = digestblock ^ tmpf.state[i] ^ tmpf.state[i+4] ^ tmpf.state[i+8] ^ tmpf.state[i+12]
		_ = binary.Write(digest, binary.LittleEndian, digestblock)
	}
	return digest.Bytes()
}

func (f *FastHash) Hexdigest() string {
	return hex.EncodeToString(f.Digest())
}

func (f *FastHash) copy() *FastHash {
	newf := FastHash{
		state:  make([]uint32, 16),
		buffer: make([]byte, 8),
		round:  0,
	}
	copy(newf.state, f.state)
	copy(newf.buffer, f.buffer)
	newf.round = f.round
	return &newf
}

func (f *FastHash) doRound() {
	roundbuf := f.buffer[:4]
	roundstate := f.round % len(f.state)
	newstate := uint64(binary.LittleEndian.Uint32(roundbuf) >> f.round)
	newstate = newstate + 3177888673
	newstate = newstate * uint64(f.state[roundstate])
	f.state[roundstate] = uint32(newstate % 4294967291)
	f.buffer = f.buffer[4:]
	f.round = f.round + 1
}

syntax on
set backspace=2
"set background=dark
hi Folded ctermbg=0
filetype plugin indent on
set encoding=utf-8
set number relativenumber
set cursorline
set t_Co=256
set clipboard=unnamedplus
set ruler
set path+=**

set foldmethod=indent

"Tabs and spacing
set autoindent
set cindent
set tabstop=4
set expandtab
set shiftwidth=4
set smarttab
nnoremap tn :tabnew<Space>
nnoremap <C-Tab> :tabn<CR>
nnoremap <C-S-Tab> :tabp<CR>
nnoremap tf :tabfirst<CR>
nnoremap tl :tablast<CR>

"Search
set hlsearch
set incsearch
set ignorecase
set smartcase
"set diffopt +=iwhite


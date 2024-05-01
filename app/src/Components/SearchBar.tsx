import React, { useState } from 'react'
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { InputText } from "primereact/inputtext";
import { address } from '../util/webAddress';

import axios from 'axios';

type Props = {
  setChosenWord: (word: string) => void;
}

const SearchBar = ({ setChosenWord }: Props) => {
  const [value, setValue] = useState<string>('');
  const [searchResults, setSearchResults] = useState<string[]>([])

  const handleSearch = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const searchTerm = e.target.value;
    setValue(searchTerm);

    try {
      const response = await axios.get(`${address}/search_word?word=${searchTerm}`);
      const matchingWords = response.data.matching_words;
      setSearchResults(matchingWords)
      console.log('Matching words:', matchingWords);
    } catch (error) {
      console.error('Error fetching matching words:', error);
    }
  };

  const handleSearchResultClick = (chosenWord: any) => {
    const result = chosenWord;
    setValue("");
    setSearchResults([])
    setChosenWord(result.code);
  }

  // const handleSearchButtonClick = () => {
  //   const chosenWord = value
  //   setValue("");
  //   setSearchResults([]);
  //   setChosenWord(chosenWord);
  // };

  return (
    <div className="search-bar">
      <span className="p-input-icon-left">
        <i className="pi pi-search" />
        <InputText
          placeholder="Search Words"
          className="searchBar"
          style={{ minWidth:'430px' }}
          value={value} // Bind the searchQuery state to the input
          onChange={(e) => handleSearch(e)}
        />
        {/* <i className="pi pi-search" style={{ fontSize: '1rem', marginRight: "2rem" }}></i> */}
      </span>
      <DataTable
        value={searchResults.map((word) => ({ code: word }))}
        className={`search-results-table`}
        style={{ width: '93%', left: '3.5%', borderRadius: '20px'}}
        selectionMode="single"
        onSelectionChange={(e) => handleSearchResultClick(e.value)}
        // stripedRows
        emptyMessage=""
      >
        <Column
          header=""
          headerStyle={{ display: "none" }}
          field="code"
        />
      </DataTable>
    </div>
  )
}

export default SearchBar
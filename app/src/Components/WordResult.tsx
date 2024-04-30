import React, { useState, useEffect } from 'react'
import axios from 'axios';
import { ProgressSpinner } from 'primereact/progressspinner';
import { Divider } from 'primereact/divider';

type Props = {
  chosenWord: string;
}

const WordResult = ({ chosenWord }: Props) => {
  const [definitions, setDefinitions] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    setErrorMessage('')
    setIsLoading(true);
    const fetchDefinitions = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/get_definitions/${chosenWord}`);
        setDefinitions(response.data.definitions.split("|"));
        console.log(response.data.definitions);
      } catch (error) {
        console.error('Error fetching matching words:', error);
        setErrorMessage("Definition not found!")
      } finally {
        setIsLoading(false);
      }
    };

    fetchDefinitions();
  }, [chosenWord]);

  const renderDefinitions = () => {
    return definitions.map((definition: string, index: number) => {
      return (<li key={index}>{definition}</li>);
    });
  };

  return (
    <div>
      {isLoading &&
        <ProgressSpinner 
        style={{ width: '50px', height: '50px' }} 
        strokeWidth="8" fill="var(--surface-ground)" 
        animationDuration=".5s" />
      }
      {errorMessage !== '' ? (
        <div>{errorMessage}</div>
      ) : (
        <div className='wordResults' style={{ textAlign: 'left' }}>
          <span className='wordBeingDefined'>
            <b style={{fontSize: "1em"}}>{chosenWord}</b>
            <Divider type="solid" />
          </span>
          

          <div className='definitionsBeingRendered'>
            <ol>{renderDefinitions()}</ol>
          </div>

        </div>
      )}

    </div>
  );
}

export default WordResult
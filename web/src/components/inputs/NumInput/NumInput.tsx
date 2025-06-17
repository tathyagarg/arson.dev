import { useRef, useState } from 'react';
import './NumInput.module.css'

const NumInput = () => {
  const [value, setValue] = useState('1');
  const spanRef = useRef(null);

  return <>
    <input
      type='text'
      className='text-text px-2 py-1 rounded-md max-w-16'
      value={value}
      onChange={(e) => setValue(e.target.value)}
      style={{
        width: spanRef.current ? `${spanRef.current.offsetWidth + 12}px` : 'auto'
      }}
    />
    <span ref={spanRef} className="absolute invisible">{value}</span>
  </>
}

export default NumInput;

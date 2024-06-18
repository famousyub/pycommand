{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE OverloadedStrings #-}
import Network(PortID(PortNumber),connectTo)
import Network.Socket hiding (recv)
import Network.Socket.ByteString (recv, sendAll)
import System.IO hiding (hPutStrLn,hPutStr)
import Data.ByteString.Char8 hiding (zip,drop,map,unlines,putStrLn,putStr,head)
import qualified Data.ByteString as S
import Control.Concurrent
import Foreign(Ptr,Word8,free,mallocBytes)
import Foreign.C.Types(CChar)
import Control.Monad.Reader
import Control.Exception
import Text.Printf(printf)
import Prelude hiding (catch,log)

receiveBufSize = 4096 :: Int
connectionTimeout = 2000

main = sendMessage "localhost" [0x4,0x3] >>= print

sendMessage :: String -> [Word8] -> IO (Maybe S.ByteString)
sendMessage host msg = bracket connect disconnect loop
  where
    disconnect = hClose
    loop st    = catch (run (S.pack msg) st) (\(_ :: IOException) -> return Nothing)
    connect = notify $ do
        h <- connectTo (host) (PortNumber $ fromIntegral 6666)
        hSetBuffering h NoBuffering
        return h
    notify = bracket_ (printf "Connecting to %s ... " host >> hFlush stdout) (putStrLn "done.")

run :: S.ByteString -> Handle -> IO (Maybe S.ByteString)
run msg h = do
    print "running all things..."
    m <- newEmptyMVar
    forkIO $ (listenForResponse h m)
    -- putStrLn "hickup"  -- needed on linux 64bit ghc 7.0.2
    n <- pushOutMessage msg h m
    print "going on..."
    ss <- takeMVar m 
    return ss
  where
    pushOutMessage :: S.ByteString -> Handle -> MVar (Maybe S.ByteString) -> IO (MVar (Maybe S.ByteString))
    pushOutMessage msg h m = do
        S.putStrLn "pushing out the message.............."
        -- next line causes a "resource vanished (Connection reset by peer)" on mac os X ghci 7.0.2 echoServer
        putStrLn ("sending --> " ++ show msg)
        hPutStr h msg
        hFlush h -- Make sure that we send data immediately
        return m

listenForResponse ::  Handle -> MVar (Maybe S.ByteString) -> IO ()
listenForResponse h m = do  putStrLn "listening for response..."
                            msg <- receiveResponse h
                            putMVar m msg
                            return ()
  where

    receiveResponse :: Handle -> IO (Maybe S.ByteString)
    receiveResponse h = do
        buf <- mallocBytes receiveBufSize
        dataResp <- receiveMsg buf h
        free buf
        return dataResp

    receiveMsg :: Ptr CChar -> Handle -> IO (Maybe S.ByteString)
    receiveMsg buf h = do
        putStrLn ("wait for data with timeout:" ++ show connectionTimeout ++ " ms\n")
        dataAvailable <- waitForData h connectionTimeout
        if not dataAvailable then (print "no message available...") >> return Nothing
          else do
            answereBytesRead <- hGetBufNonBlocking h buf receiveBufSize
            Just `fmap` S.packCStringLen (buf,answereBytesRead)

    waitForData ::  Handle -> Int -> IO (Bool)
    waitForData h waitTime_ms = do
      S.putStr "."
      inputAvailable <- hWaitForInput h 10
      if inputAvailable then return True 
        else if waitTime_ms > 0
              then waitForData h (waitTime_ms - 10)
              else return False
                